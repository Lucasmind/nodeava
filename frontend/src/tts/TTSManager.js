import { config } from '../app/config.js';
import { log, error, warn } from '../utils/logger.js';

export class TTSManager {
  constructor() {
    this.ready = false;
    this.onAudioReady = null; // callback(audioData | null) — null signals a failed sentence
    this._voice = config.ttsDefaultVoice;
    this._speed = config.ttsDefaultSpeed;
    this._abortController = null;
    this._queue = [];
    this._processing = false;
  }

  async init() {
    log('Initializing TTS (Kokoro-FastAPI container)...');
    this.ready = true;
    log('TTS ready');
  }

  synthesize(text) {
    if (!this.ready) {
      warn('TTS not ready, skipping synthesis');
      if (this.onAudioReady) this.onAudioReady(null);
      return;
    }
    if (!text?.trim()) {
      if (this.onAudioReady) this.onAudioReady(null);
      return;
    }

    this._queue.push(text);
    this._processNext();
  }

  async _processNext() {
    if (this._processing || this._queue.length === 0) return;
    this._processing = true;

    const text = this._queue.shift();
    const t0 = performance.now();
    const charCount = text.length;
    log(`TTS synthesize (${charCount} chars): "${text.substring(0, 60)}..."`);

    this._abortController = new AbortController();

    let result;
    try {
      const res = await fetch(config.ttsEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: 'kokoro',
          input: text,
          voice: this._voice,
          speed: this._speed,
          response_format: 'pcm',
          stream: false,
          return_timestamps: true,
        }),
        signal: this._abortController.signal,
      });

      if (!res.ok) {
        throw new Error(`TTS HTTP ${res.status}: ${await res.text()}`);
      }

      result = await res.json();
    } catch (err) {
      if (err.name === 'AbortError') {
        this._processing = false;
        return;
      }
      error('TTS synthesis error:', err);
      // Signal failure so Orchestrator can decrement _pendingSentences
      if (this.onAudioReady) this.onAudioReady(null);
      this._processing = false;
      this._processNext();
      return;
    }

    const elapsed = (performance.now() - t0).toFixed(0);
    log(`TTS audio ready in ${elapsed}ms (${charCount} chars): "${text.substring(0, 40)}..."`);

    const audioData = this._transformResponse(result);
    if (this.onAudioReady) {
      this.onAudioReady(audioData);
    }

    this._processing = false;
    this._processNext();
  }

  _transformResponse(result) {
    // Decode base64 PCM audio to ArrayBuffer
    const binaryStr = atob(result.audio);
    const bytes = new Uint8Array(binaryStr.length);
    for (let i = 0; i < binaryStr.length; i++) {
      bytes[i] = binaryStr.charCodeAt(i);
    }
    const audioBuffer = bytes.buffer;

    // Map timestamps to TalkingHead's expected format
    const words = [];
    const wtimes = [];
    const wdurations = [];

    if (result.timestamps) {
      for (const ts of result.timestamps) {
        words.push(ts.word);
        wtimes.push(ts.start_time * 1000);       // seconds → ms
        wdurations.push((ts.end_time - ts.start_time) * 1000);
      }
    }

    return {
      audio: [audioBuffer],  // Array of ArrayBuffer — TalkingHead concatenates + converts PCM
      words,
      wtimes,
      wdurations,
    };
  }

  setVoice(voiceName) {
    this._voice = voiceName;
    log(`TTS voice set to: ${voiceName}`);
  }

  setSpeed(speed) {
    this._speed = speed;
  }

  clear() {
    this._queue = [];
    if (this._abortController) {
      this._abortController.abort();
      this._abortController = null;
    }
  }

  get isReady() {
    return this.ready;
  }
}
