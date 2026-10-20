---
name: product-domain
description: Product/vision thinking for this user's projects — how to reason about the products they build (fountain's QR web app, vibeos's OS + SDK), their users, and roadmap at a senior-product level. Use when discussing what to build, product decisions, features, UX tradeoffs, or future direction. Triggers: 'product', 'vision', 'roadmap', 'should we build', 'features', 'users', 'what's the point of', 'direction'.
---

# Product Domain Thinking

## The user's product landscape (working assumptions from the codebase — user corrects if wrong)

1. **fountain** — QR-code web app (sender + receiver flows; likely pair/share/transfer — send data via QR, receive at the other end). Mobile-friendly camera over HTTPS (hence .certs/). Separate "web app/" static directory (photo gallery + audio) suggests a consumer-facing gallery/experience page. Product angles: zero-install transfer, offline capability, privacy (QR = no account, no server in the middle).
2. **vibeos** — custom x86 OS with a user-app SDK (callbacks, windows, drawing, keyboard/mouse). Systems playground/portfolio piece. SDK guide in Italian hints at a personal/educational angle (learning or Italian-speaking friends).

## Product thinking rules

1. **fountain (consumer/utility web)**
   - Solvability first: does the flow work in <3 steps, under 30 seconds, on a phone camera?
   - Perfect scan reliability beats features. Scanning fails = product failure.
   - Offline/accountless is a feature: keep the server out of the flow where possible.
   - Receiver side must not assume a desktop; design for phone-to-phone.
2. **vibeos (developer/systems product)**
   - The SDK is the product: developer experience (callbacks, window lifecycle, painting) makes or breaks it.
   - Demo-ability: a calculator is fine, but a demo showcasing graphics/physics/multitasking sells the OS.
   - Compatibility guardrails: kernel improvements must not silently break the documented SDK contract (SDK_GUIDE.md).
3. "Should we build X?" — give a recommendation with reasoning; they want a product person's opinion, not a menu of options.

## Roadmap altitude
- fountain: (1) rock-solid round-trip scan → (2) one killer scenario demoed end-to-end → (3) then new capabilities. Test via test-roundtrip.mjs + Playwright + real camera (controlmcp on Safari/Chrome).
- vibeos: keep kernel stable while growing the SDK surface; each SDK addition ships with a demo app — the OS is the demo of the SDK's power.

## How to talk products with this user
- Direct, opinionated, no buzzwords ("synergy", "paradigm" → banned).
- Concrete tradeoffs over abstract principles; tie every idea to "who uses it and when".
- They value real working things — demos, running code, visible progress — over forecasts and decks.
