import { config } from '../../app/config.js';

const VOICE_OPTIONS = [
  { value: 'af_bella', label: 'Bella (F, US)' },
  { value: 'af_nova', label: 'Nova (F, US)' },
  { value: 'af_sarah', label: 'Sarah (F, US)' },
  { value: 'am_fenrir', label: 'Fenrir (M, US)' },
  { value: 'am_adam', label: 'Adam (M, US)' },
  { value: 'am_michael', label: 'Michael (M, US)' },
  { value: 'bf_emma', label: 'Emma (F, UK)' },
  { value: 'bm_george', label: 'George (M, UK)' },
];

export class ControlPanel {
  constructor(containerEl) {
    this.container = containerEl;
    this.onSpeak = null;       // callback(text)
    this.onVoiceChange = null; // callback(voiceName)
    this.onMicToggle = null;   // callback(active)
    this.micActive = false;
    this.build();
  }

  build() {
    // Text input row
    const row = document.createElement('div');
    row.className = 'text-input-row';

    this.textInput = document.createElement('input');
    this.textInput.id = 'text-input';
    this.textInput.type = 'text';
    this.textInput.placeholder = 'Type a message...';
    this.textInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && this.textInput.value.trim()) {
        this.handleSpeak();
      }
    });

    this.speakBtn = document.createElement('button');
    this.speakBtn.className = 'control-btn';
    this.speakBtn.textContent = 'Speak';
    this.speakBtn.addEventListener('click', () => this.handleSpeak());

    row.appendChild(this.textInput);
    row.appendChild(this.speakBtn);

    // Mic button
    this.micBtn = document.createElement('button');
    this.micBtn.className = 'control-btn';
    this.micBtn.textContent = 'Mic Off';
    this.micBtn.addEventListener('click', () => this.toggleMic());

    // Voice selector
    this.voiceSelect = document.createElement('select');
    this.voiceSelect.className = 'control-select';
    for (const opt of VOICE_OPTIONS) {
      const option = document.createElement('option');
      option.value = opt.value;
      option.textContent = opt.label;
      this.voiceSelect.appendChild(option);
    }
    this.voiceSelect.value = config.ttsDefaultVoice;
    this.voiceSelect.addEventListener('change', () => {
      if (this.onVoiceChange) this.onVoiceChange(this.voiceSelect.value);
    });

    this.container.appendChild(row);
    this.container.appendChild(this.micBtn);
    this.container.appendChild(this.voiceSelect);
  }

  handleSpeak() {
    const text = this.textInput.value.trim();
    if (!text) return;
    if (this.onSpeak) this.onSpeak(text);
    this.textInput.value = '';
  }

  toggleMic() {
    this.micActive = !this.micActive;
    this.micBtn.textContent = this.micActive ? 'Mic On' : 'Mic Off';
    this.micBtn.classList.toggle('active', this.micActive);
    if (this.onMicToggle) this.onMicToggle(this.micActive);
  }

  setMicState(active) {
    this.micActive = active;
    this.micBtn.textContent = active ? 'Mic On' : 'Mic Off';
    this.micBtn.classList.toggle('active', active);
  }

  setSpeakEnabled(enabled) {
    this.speakBtn.disabled = !enabled;
    this.textInput.disabled = !enabled;
  }

  setMicEnabled(enabled) {
    this.micBtn.disabled = !enabled;
  }
}
