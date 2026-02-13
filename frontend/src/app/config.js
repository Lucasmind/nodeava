export const config = {
  // Service endpoints (proxied through nginx in production)
  sttEndpoint: '/api/stt/v1/audio/transcriptions',
  llmEndpoint: '/api/llm/v1/chat/completions',
  ttsEndpoint: '/api/tts/dev/captioned_speech',

  // LLM settings (temperature is set server-side for thinking model compatibility)
  llmModel: 'default',
  llmMaxTokens: 1024,
  systemPrompt: `Your name is Ava. You are a friendly, expressive conversational assistant embodied as a 3D avatar. Match your response length to the request — brief for simple questions, detailed for complex ones or when asked to elaborate.

You MUST begin every response with exactly one emotion tag in brackets. Available emotions: [neutral], [happy], [sad], [angry], [fear], [disgust], [love], [sleep].

Examples:
[happy] Hey! Great to see you!
[neutral] The capital of France is Paris.
[sad] I'm sorry to hear that happened.

Important: Always include the emotion tag. Never skip it.`,

  // Avatar settings
  avatarUrl: '/avatars/default-avatar.glb',
  avatarBody: 'F',
  initialMood: 'neutral',
  cameraView: 'upper',

  // TTS settings
  ttsDefaultVoice: 'af_bella',
  ttsDefaultSpeed: 1,
  ttsVoices: ['af_bella', 'am_fenrir', 'af_nova', 'bf_emma', 'bm_george'],

  // VAD settings
  vadPositiveThreshold: 0.4,
  vadNegativeThreshold: 0.25,
  vadRedemptionMs: 1400,
  vadMinSpeechMs: 400,
  vadPreSpeechPadMs: 800,

  // Audio settings
  pcmSampleRate: 24000,
};
