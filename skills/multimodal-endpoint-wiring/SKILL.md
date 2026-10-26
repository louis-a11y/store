---
name: multimodal-endpoint-wiring
description: Configure free multimodal endpoints (image-gen, audio, TTS) using Gemini + OpenRouter; notes what's missing. Triggers: wire multimodal, add endpoint, enable image gen, setup voice.
---
# Multimodal Endpoint Wiring (Gap-Fill)

Missing pieces (free paths to configure):
- Image generation: OpenRouter `flux` (free tier) or Gemini `imagen`; add endpoint URL to `omoc.jsonc` / agent `multimodal-worker`
- Voice/TTS: Gemini TTS endpoint; OpenRouter text-to-speech models; configure `system_prompt_template` for voice mode
- Audio transcription already wired (`whisper` local); just need source file path

Action: edit `opencode.jsonc` agent `multimodal-worker` to include endpoint URLs when you find free sources; never call paid endpoints without confirming funded key.

Sources: your store (`louis-a11y/store`) + free repos.
