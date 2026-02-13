export class SubtitleOverlay {
  constructor(containerEl) {
    this.container = containerEl;
    this.currentLine = null;
    this.fadeTimer = null;
  }

  showUser(text) {
    this.finalizeCurrent();
    const line = document.createElement('div');
    line.className = 'subtitle-text user';
    line.textContent = text;
    this.container.appendChild(line);
    this.scheduleCleanup();
  }

  startAssistant() {
    this.finalizeCurrent();
    this.currentLine = document.createElement('div');
    this.currentLine.className = 'subtitle-text assistant';
    this.container.appendChild(this.currentLine);
  }

  appendAssistant(word) {
    if (!this.currentLine) this.startAssistant();
    this.currentLine.textContent += word;
  }

  finalizeCurrent() {
    this.currentLine = null;
  }

  clear() {
    this.currentLine = null;
    while (this.container.firstChild) {
      this.container.removeChild(this.container.firstChild);
    }
  }

  scheduleCleanup() {
    if (this.fadeTimer) clearTimeout(this.fadeTimer);
    this.fadeTimer = setTimeout(() => {
      // Remove old lines, keep last 3
      while (this.container.children.length > 3) {
        this.container.removeChild(this.container.firstChild);
      }
    }, 10000);
  }
}
