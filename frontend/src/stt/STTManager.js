import { MicVAD } from '@ricky0123/vad-web';
import { float32ToWav } from '../utils/audio-utils.js';
import { config } from '../app/config.js';
import { log, error, warn } from '../utils/logger.js';

export class STTManager {
  constructor() {
    this.vad = null;
    this.listening = false;
    this.initializing = false;
    this.onTranscription = null;  // callback(text)
    this.onSpeechStart = null;    // callback()
    this.onSpeechEnd = null;      // callback()
    this.onError = null;          // callback(err)
  }

  /**
   * Lazily initialize VAD + mic on first use.
   * This avoids prompting for mic permission on page load.
   */
  async ensureInitialized() {
    if (this.vad || this.initializing) return;
    this.initializing = true;

    log('Initializing VAD + STT (requesting mic access)...');

    try {
      this.vad = await MicVAD.new({
        baseAssetPath: '/vad/',
        onnxWASMBasePath: '/vad/',
        positiveSpeechThreshold: config.vadPositiveThreshold,
        negativeSpeechThreshold: config.vadNegativeThreshold,
        redemptionFrames: 8,
        minSpeechFrames: 3,
        preSpeechPadFrames: 1,

        onSpeechStart: () => {
          log('Speech detected');
          if (this.onSpeechStart) this.onSpeechStart();
        },

        onSpeechEnd: async (audio) => {
          log(`Speech ended, ${audio.length} samples`);
          if (this.onSpeechEnd) this.onSpeechEnd();
          await this.transcribe(audio);
        },

        onVADMisfire: () => {
          log('VAD misfire (too short)');
        },
      });

      log('VAD initialized');
    } catch (err) {
      error('VAD initialization failed:', err);
      this.initializing = false;
      throw err;
    }
  }

  async start() {
    try {
      await this.ensureInitialized();
    } catch (err) {
      if (this.onError) this.onError(err);
      return;
    }

    this.vad.start();
    this.listening = true;
    log('Listening started');
  }

  pause() {
    if (!this.vad) return;
    this.vad.pause();
    this.listening = false;
    log('Listening paused');
  }

  async transcribe(audioFloat32) {
    try {
      const wavBuffer = float32ToWav(audioFloat32, 16000);
      const wavBlob = new Blob([wavBuffer], { type: 'audio/wav' });

      const formData = new FormData();
      formData.append('file', wavBlob, 'audio.wav');
      formData.append('model', 'whisper-1');
      formData.append('response_format', 'json');

      const response = await fetch(config.sttEndpoint, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`STT HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      const text = result.text?.trim();

      if (text) {
        log(`Transcription: "${text}"`);
        if (this.onTranscription) this.onTranscription(text);
      } else {
        log('Empty transcription');
      }
    } catch (err) {
      error('Transcription failed:', err);
      if (this.onError) this.onError(err);
    }
  }

  get isListening() {
    return this.listening;
  }
}
