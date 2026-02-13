import { Orchestrator } from './pipeline/Orchestrator.js';
import { UIManager } from './ui/UIManager.js';
import { log, error } from './utils/logger.js';

const orchestrator = new Orchestrator();
window.__orch = orchestrator; // debug access
let ui = null;

async function boot() {
  const container = document.getElementById('avatar-container');
  const loadingOverlay = createLoadingOverlay();
  document.body.appendChild(loadingOverlay);

  try {
    await orchestrator.init(container, (text, pct) => {
      updateLoading(loadingOverlay, text, pct);
    });

    ui = new UIManager(orchestrator);
    ui.init();

    await sleep(400);
    loadingOverlay.classList.add('hidden');
    setTimeout(() => loadingOverlay.remove(), 500);

    document.addEventListener('visibilitychange', () => {
      orchestrator.handleVisibility(document.visibilityState === 'visible');
    });

    log('Boot complete — all systems ready');
  } catch (err) {
    error('Boot failed:', err);
    updateLoading(loadingOverlay, `Error: ${err.message}`, 0);
  }
}

function createLoadingOverlay() {
  const overlay = document.createElement('div');
  overlay.className = 'loading-overlay';

  const text = document.createElement('div');
  text.className = 'loading-text';
  text.textContent = 'Loading...';

  const bar = document.createElement('div');
  bar.className = 'loading-bar';

  const fill = document.createElement('div');
  fill.className = 'loading-bar-fill';

  bar.appendChild(fill);
  overlay.appendChild(text);
  overlay.appendChild(bar);

  return overlay;
}

function updateLoading(overlay, text, pct) {
  const textEl = overlay.querySelector('.loading-text');
  const fillEl = overlay.querySelector('.loading-bar-fill');
  if (textEl) textEl.textContent = text;
  if (fillEl) fillEl.style.width = `${pct}%`;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

boot();
