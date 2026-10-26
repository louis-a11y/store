---
name: multimodal-extension
description: Enables image/audio/video/transcription via free providers (Gemini + OpenRouter); no paid tiers. Triggers: generate image, describe audio, transcribe, voice, multimodal.
---
# Multimodal Extension (Free-Only Config)

Config sources (all free):
- Images: OpenRouter `flux` / Gemini `imagen`; local `~/bin/vimg` for OCR/reading
- Audio transcription: local `whisper` (open-source STT)
- Voice/text: Gemini + OpenRouter text endpoints (already working)

To activate per agent, add to opencode.jsonc:
  "multimodal": {"images": true, "audio_transcription": true, "voice": false},
  "system_prompt_template": "<<< MULTIMODAL PROMPT >>>"

Sub-agent for execution (add manually):
  "multimodal-worker": {"description":"Multimodal pipeline worker","mode":"subagent","prompt":"Use local vimg/OCR for images, whisper for audio, and Gemini/OR for generation.","models":["google/gemini-3-flash-preview","openrouter/minimax/minimax-m3.1-flash:free"],"reasoning":"low","system_prompt_template":"<<< FULL MULTIMODAL INSTRUCTION >>>"}
