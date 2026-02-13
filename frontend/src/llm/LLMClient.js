import { config } from '../app/config.js';
import { log, error } from '../utils/logger.js';

export class LLMClient {
  constructor() {
    this.abortController = null;
  }

  /**
   * Send a streaming chat completion request.
   * @param {Array} messages - OpenAI-format messages [{role, content}]
   * @param {function} onToken - callback(tokenStr) for each streamed token
   * @param {function} onDone - callback(fullText) when stream completes
   * @param {function} onError - callback(err)
   */
  async chatCompletion(messages, onToken, onDone, onError) {
    this.abort(); // Cancel any in-flight request

    this.abortController = new AbortController();

    try {
      const response = await fetch(config.llmEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        signal: this.abortController.signal,
        body: JSON.stringify({
          model: config.llmModel,
          messages,
          max_tokens: config.llmMaxTokens,
          stream: true,
        }),
      });

      if (!response.ok) {
        const err = new Error(`LLM HTTP ${response.status}: ${response.statusText}`);
        err.status = response.status;
        throw err;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullText = '';
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // Keep incomplete line

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || !trimmed.startsWith('data: ')) continue;

          const data = trimmed.slice(6);
          if (data === '[DONE]') continue;

          try {
            const parsed = JSON.parse(data);
            const delta = parsed.choices?.[0]?.delta?.content;
            if (delta) {
              fullText += delta;
              if (onToken) onToken(delta);
            }
          } catch {
            // Skip malformed JSON lines
          }
        }
      }

      log(`LLM response: ${fullText.length} chars`);
      if (onDone) onDone(fullText);
    } catch (err) {
      if (err.name === 'AbortError') {
        log('LLM request aborted');
        return;
      }
      const classified = this._classifyError(err);
      error('LLM error:', classified.message);
      if (onError) onError(classified);
    } finally {
      this.abortController = null;
    }
  }

  _classifyError(err) {
    if (err.status === 503) {
      return new Error('LLM service is busy — try again shortly');
    }
    if (err.status === 404) {
      return new Error('LLM model not found — check model configuration');
    }
    if (err.status >= 500) {
      return new Error(`LLM server error (${err.status}) — check service logs`);
    }
    if (err.status >= 400) {
      return new Error(`LLM request error (${err.status}) — ${err.message}`);
    }
    if (err.message?.includes('Failed to fetch') || err.message?.includes('NetworkError')) {
      return new Error('Cannot reach LLM service — check if container is running');
    }
    return err;
  }

  abort() {
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = null;
    }
  }
}
