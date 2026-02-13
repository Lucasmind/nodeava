import { TalkingHead } from '@met4citizen/talkinghead';
import { config } from '../app/config.js';
import { log } from '../utils/logger.js';

export class AvatarManager {
  constructor() {
    this.head = null;
    this.container = null;
    this.loaded = false;
  }

  async init(containerEl) {
    this.container = containerEl;

    this.head = new TalkingHead(this.container, {
      ttsEndpoint: null,
      lipsyncModules: ['en'],
      lipsyncLang: 'en',
      cameraView: config.cameraView,
      avatarMood: config.initialMood,
      avatarIdleEyeContact: 0.3,
      avatarSpeakingEyeContact: 0.6,
      avatarIdleHeadMove: 0.5,
      avatarSpeakingHeadMove: 0.5,
      pcmSampleRate: config.pcmSampleRate,
      modelFPS: 30,
      cameraRotateEnable: true,
      cameraPanEnable: false,
      cameraZoomEnable: false,
      lightAmbientIntensity: 2,
      lightDirectIntensity: 30,
    });

    log('AvatarManager initialized');
  }

  async loadAvatar(url = config.avatarUrl, onProgress = null) {
    if (!this.head) throw new Error('AvatarManager not initialized');

    log(`Loading avatar: ${url}`);

    await this.head.showAvatar(
      {
        url,
        body: config.avatarBody,
        avatarMood: config.initialMood,
        lipsyncLang: 'en',
      },
      onProgress
    );

    this.loaded = true;
    log('Avatar loaded');
  }

  setMood(mood) {
    if (!this.head || !this.loaded) return;
    this.head.setMood(mood);
  }

  setView(view, opts = {}) {
    if (!this.head) return;
    this.head.setView(view, opts);
  }

  speakAudio(audioData, opts = {}, onSubtitles = null) {
    if (!this.head || !this.loaded) return;
    this.head.speakAudio(audioData, opts, onSubtitles);
  }

  stopSpeaking() {
    if (!this.head) return;
    try {
      this.head.stopSpeaking();
    } catch {
      // May not have stopSpeaking — TalkingHead uses speech queue
    }
  }

  lookAtCamera(durationMs = 1000) {
    if (!this.head) return;
    this.head.lookAtCamera(durationMs);
  }

  start() {
    if (this.head) this.head.start();
  }

  stop() {
    if (this.head) this.head.stop();
  }

  get audioCtx() {
    return this.head?.audioCtx || null;
  }

  get isLoaded() {
    return this.loaded;
  }
}
