import { AvatarManager } from '../avatar/AvatarManager.js';
import { TTSManager } from '../tts/TTSManager.js';
import { STTManager } from '../stt/STTManager.js';
import { LLMClient } from '../llm/LLMClient.js';
import { ConversationManager } from '../llm/ConversationManager.js';
import { EmotionController } from '../avatar/EmotionController.js';
import { StateMachine, States } from '../app/state.js';
import { config } from '../app/config.js';
import { log, error, warn } from '../utils/logger.js';

// Sentence boundary: period/exclamation/question after a word character (avoids "1. ")
const SENTENCE_END_RE = /(?<=[a-zA-Z,\])"'])[.!?]\s+/;
const MAX_RETRIES = 2;
const RETRY_DELAY_MS = 1000;

// Qwen3 thinking tags: <think>...</think> followed by the actual response
const THINK_OPEN = '<think>';
const THINK_CLOSE = '</think>';
// Regex to strip <think>...</think> blocks from full text (for history cleanup)
const THINK_BLOCK_RE = /<think>[\s\S]*?<\/think>\s*/g;
// Strip emojis so TTS doesn't read them aloud as descriptions
const EMOJI_RE = /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F1E0}-\u{1F1FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{FE00}-\u{FE0F}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{200D}\u{20E3}\u{E0020}-\u{E007F}]+/gu;

// Clean text for TTS: strip markdown and emojis so they aren't read aloud
function cleanForTTS(text) {
  return text
    .replace(EMOJI_RE, '')             // emojis
    .replace(/\*\*(.+?)\*\*/g, '$1')  // **bold** → bold
    .replace(/\*(.+?)\*/g, '$1')      // *italic* → italic
    .replace(/^#{1,6}\s+/gm, '')      // ### headings
    .replace(/^---+$/gm, '')          // --- horizontal rules
    .replace(/^[-*+]\s+/gm, '')       // - bullet points
    .replace(/^\d+\.\s+/gm, '')       // 1. numbered lists
    .replace(/`([^`]+)`/g, '$1')      // `code` → code
    .replace(/\s{2,}/g, ' ')          // collapse whitespace
    .trim();
}

export class Orchestrator {
  constructor() {
    this.avatar = new AvatarManager();
    this.tts = new TTSManager();
    this.stt = new STTManager();
    this.llm = new LLMClient();
    this.conversation = new ConversationManager();
    this.emotion = null;
    this.state = new StateMachine();

    // Callbacks for UI updates
    this.onStateChange = null;
    this.onUserSpeech = null;
    this.onAssistantToken = null;
    this.onAssistantSentence = null;
    this.onAssistantDone = null;
    this.onError = null;

    // Streaming state
    this._rawBuffer = '';        // accumulates all tokens for thinking detection
    this._tokenBuffer = '';      // holds filtered text for sentence splitting
    this._isThinking = false;    // true while inside <think>...</think>
    this._thinkingDone = false;  // true once thinking phase resolved (detected or skipped)
    this._emotionParsed = false;
    this._currentEmotion = null;
    this._pendingSentences = 0;
    this._llmDone = false;
  }

  async init(containerEl, onProgress = null) {
    this.state.onChange = (newState, oldState) => {
      if (this.onStateChange) this.onStateChange(newState, oldState);
    };

    // 1. Avatar
    if (onProgress) onProgress('Initializing avatar...', 5);
    await this.avatar.init(containerEl);

    if (onProgress) onProgress('Loading avatar model...', 15);
    await this.avatar.loadAvatar(config.avatarUrl, (ev) => {
      if (ev.lengthComputable && onProgress) {
        const pct = 15 + Math.round((ev.loaded / ev.total) * 30);
        onProgress('Loading avatar model...', pct);
      }
    });

    this.emotion = new EmotionController(this.avatar);

    // 2. TTS
    if (onProgress) onProgress('Loading TTS engine...', 50);
    await this.tts.init((progress) => {
      if (progress?.progress != null && onProgress) {
        const pct = 50 + Math.round(progress.progress * 30);
        onProgress('Loading TTS model...', pct);
      }
    });

    // Wire TTS audio output → avatar lip sync
    this.tts.onAudioReady = (audioData) => {
      if (audioData) {
        this.avatar.speakAudio(audioData, {}, (word) => {
          if (this.onAssistantToken) this.onAssistantToken(word);
        });
      }

      // Track when sentences finish (null = TTS failed, still count it)
      this._pendingSentences--;
      if (this._pendingSentences <= 0 && this._llmDone) {
        this._finishSpeaking();
      }
    };

    // 3. STT (VAD) — initialized lazily on first mic enable to avoid
    // prompting for mic permission on page load
    this.stt.onSpeechStart = () => {
      // Barge-in: interrupt avatar if speaking
      if (this.state.is(States.SPEAKING) || this.state.is(States.THINKING)) {
        this.interrupt();
      }
      this.state.transition(States.LISTENING);
    };

    this.stt.onSpeechEnd = () => {
      this.state.transition(States.TRANSCRIBING);
    };

    this.stt.onTranscription = (text) => {
      this.handleUserInput(text);
    };

    this.stt.onError = (err) => {
      error('STT error:', err);
      this.state.transition(States.IDLE);
      if (this.onError) this.onError(`STT error: ${err.message}`);
    };

    if (onProgress) onProgress('Ready!', 100);
    log('Orchestrator initialized');
  }

  async handleUserInput(text) {
    if (!text?.trim()) return;

    log(`User: "${text}"`);
    if (this.onUserSpeech) this.onUserSpeech(text);

    // Interrupt any in-progress response
    if (!this.state.is(States.IDLE) && !this.state.is(States.LISTENING)) {
      this.interrupt();
    }

    this.conversation.addUserMessage(text);
    this.state.transition(States.THINKING);

    this._rawBuffer = '';
    this._tokenBuffer = '';
    this._isThinking = false;
    this._thinkingDone = false;
    this._emotionParsed = false;
    this._currentEmotion = null;
    this._pendingSentences = 0;
    this._llmDone = false;

    await this._callLLMWithRetry(MAX_RETRIES);
  }

  async _callLLMWithRetry(retriesLeft) {
    const messages = this.conversation.getMessagesForAPI();

    try {
      await this.llm.chatCompletion(
        messages,
        (token) => this._handleStreamToken(token),
        (fullText) => this._handleStreamDone(fullText),
        (err) => {
          throw err;
        }
      );
    } catch (err) {
      if (err?.name === 'AbortError') return;

      if (retriesLeft > 0) {
        warn(`LLM error, retrying (${retriesLeft} left)...`, err.message);
        await this._sleep(RETRY_DELAY_MS);
        if (!this.state.is(States.THINKING)) return; // User may have interrupted
        return this._callLLMWithRetry(retriesLeft - 1);
      }

      error('LLM failed after retries:', err);
      this.state.transition(States.IDLE);
      if (this.onError) this.onError(`LLM error: ${err.message}`);
    }
  }

  _handleStreamToken(token) {
    this._rawBuffer += token;

    // Phase 1: Detect if this is a thinking model response
    if (!this._thinkingDone) {
      if (!this._isThinking && this._rawBuffer.startsWith(THINK_OPEN)) {
        this._isThinking = true;
        log('Detected thinking model, filtering <think> tokens');
      } else if (!this._isThinking && this._rawBuffer.length >= THINK_OPEN.length) {
        // Past detection window with no <think> tag — normal model
        this._thinkingDone = true;
        this._tokenBuffer = this._rawBuffer;
        log('Normal model detected, passing tokens through');
      } else if (!this._isThinking) {
        // Still accumulating for detection — don't emit yet
        return;
      }

      // Inside thinking: wait for </think> close tag
      if (this._isThinking) {
        const closeIdx = this._rawBuffer.indexOf(THINK_CLOSE);
        if (closeIdx === -1) return; // still thinking
        this._thinkingDone = true;
        this._tokenBuffer = this._rawBuffer.slice(closeIdx + THINK_CLOSE.length).replace(/^\s+/, '');
        log('Thinking done, streaming final response');
      }
    } else {
      // Past detection/thinking — append new tokens directly
      this._tokenBuffer += token;
    }

    // Phase 2: Parse emotion tag from the beginning of response (once)
    if (!this._emotionParsed) {
      const { emotion, cleanText } = this.conversation.parseEmotionTag(this._tokenBuffer);
      if (emotion) {
        this._currentEmotion = emotion;
        this._emotionParsed = true;
        this.emotion.setMood(emotion);
        this._tokenBuffer = cleanText;
      } else if (this._tokenBuffer.length > 20) {
        this._emotionParsed = true;
      }
    }

    this._flushSentences();
  }

  _flushSentences() {
    let match;
    while ((match = this._tokenBuffer.match(SENTENCE_END_RE))) {
      const endIdx = match.index + match[0].length;
      const sentence = this._tokenBuffer.slice(0, endIdx).trim();
      this._tokenBuffer = this._tokenBuffer.slice(endIdx);
      if (sentence) this._enqueueTTS(sentence);
    }
  }

  _enqueueTTS(text) {
    const clean = cleanForTTS(text);
    if (!clean) return;
    this.state.transition(States.SPEAKING);
    this._pendingSentences++;
    if (this.onAssistantSentence) this.onAssistantSentence(clean);
    this.tts.synthesize(clean);
  }

  _handleStreamDone(fullText) {
    // If thinking detection didn't finish during streaming, resolve it now
    if (!this._thinkingDone) {
      const closeIdx = this._rawBuffer.indexOf(THINK_CLOSE);
      if (closeIdx !== -1) {
        this._tokenBuffer = this._rawBuffer.slice(closeIdx + THINK_CLOSE.length).replace(/^\s+/, '');
      } else {
        // No thinking tags at all — use entire raw buffer
        this._tokenBuffer = this._rawBuffer;
      }
      this._thinkingDone = true;

      // Parse emotion tag if not done yet
      if (!this._emotionParsed) {
        const { emotion, cleanText } = this.conversation.parseEmotionTag(this._tokenBuffer);
        if (emotion) {
          this._currentEmotion = emotion;
          this._emotionParsed = true;
          this.emotion.setMood(emotion);
          this._tokenBuffer = cleanText;
        }
      }
    }

    // Flush remaining text through the same cleanup path
    const remaining = this._tokenBuffer.trim();
    if (remaining) {
      this._enqueueTTS(remaining);
    }
    this._tokenBuffer = '';
    this._llmDone = true;

    // Strip <think>...</think> blocks from full text for conversation history
    const responseText = fullText.replace(THINK_BLOCK_RE, '').trim();
    const { cleanText } = this.conversation.parseEmotionTag(responseText);
    this.conversation.addAssistantMessage(cleanText);

    if (this.onAssistantDone) this.onAssistantDone(cleanText);

    // If no sentences were queued, go idle immediately
    if (this._pendingSentences <= 0) {
      this._finishSpeaking();
    }
  }

  _finishSpeaking() {
    // Brief pause after last audio before transitioning to idle
    setTimeout(() => {
      if (this.state.is(States.SPEAKING)) {
        this.state.transition(States.IDLE);
      }
    }, 200);
  }

  interrupt() {
    log('Interrupting...');
    this.llm.abort();
    this.tts.clear();
    this.avatar.stopSpeaking();
    this._rawBuffer = '';
    this._tokenBuffer = '';
    this._pendingSentences = 0;
    this._llmDone = false;
  }

  startListening() {
    this.stt.start();
    this.state.transition(States.LISTENING);
  }

  stopListening() {
    this.stt.pause();
    if (this.state.is(States.LISTENING)) {
      this.state.transition(States.IDLE);
    }
  }

  setVoice(voice) {
    this.tts.setVoice(voice);
  }

  handleVisibility(visible) {
    if (visible) {
      this.avatar.start();
    } else {
      this.avatar.stop();
    }
  }

  _sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
