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
      throw this._classifyError(err, 'init');
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
        const err = new Error(`STT HTTP ${response.status}: ${response.statusText}`);
        err.status = response.status;
        throw err;
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
      const classified = this._classifyError(err, 'transcribe');
      error('Transcription failed:', classified.message);
      if (this.onError) this.onError(classified);
    }
  }

  _classifyError(err, context) {
    if (context === 'init') {
      if (err.name === 'NotAllowedError' || err.message?.includes('Permission denied')) {
        return new Error('Microphone permission denied — allow mic access and try again');
      }
      if (err.name === 'NotFoundError') {
        return new Error('No microphone found — connect a microphone and try again');
      }
      return new Error(`Mic initialization failed: ${err.message}`);
    }
    if (err.status === 503) return new Error('STT service is busy — try again shortly');
    if (err.status >= 500) return new Error(`STT server error (${err.status}) — check service logs`);
    if (err.message?.includes('Failed to fetch') || err.message?.includes('NetworkError')) {
      return new Error('Cannot reach STT service — check if container is running');
    }
    return err;
  }

  get isListening() {
    return this.listening;
  }
}
