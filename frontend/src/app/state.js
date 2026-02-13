import { log } from '../utils/logger.js';

export const States = {
  IDLE: 'idle',
  LISTENING: 'listening',
  TRANSCRIBING: 'transcribing',
  THINKING: 'thinking',
  SPEAKING: 'speaking',
};

export class StateMachine {
  constructor() {
    this.state = States.IDLE;
    this.onChange = null; // callback(newState, oldState)
  }

  transition(newState) {
    if (newState === this.state) return;
    const old = this.state;
    this.state = newState;
    log(`State: ${old} → ${newState}`);
    if (this.onChange) this.onChange(newState, old);
  }

  is(state) {
    return this.state === state;
  }

  get current() {
    return this.state;
  }
}
