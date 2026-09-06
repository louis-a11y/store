---
name: product-domain
description: Product/vision thinking for this user's projects — how to reason about the products they build (fountain's QR web app, vibeos's OS + SDK), their users, and roadmap at a senior-product level. Use when discussing what to build, product decisions, features, UX tradeoffs, or future direction. Triggers: 'product', 'vision', 'roadmap', 'should we build', 'features', 'users', 'what's the point of', 'direction'.
---

# Product Domain Thinking

## The user's product landscape (as currently known)
> NOTE: These are working assumptions from the codebase. If a product description is wrong, the user will correct it — treat this as the baseline, not gospel.

1. **fountain** — a QR-code web app (sender + receiver flows). Probably pair/share/transfer scenarios (send data via QR, receive at the other end). Mobile-friendly camera use over HTTPS (hence .certs/). The distinct "web app/" static directory (photo gallery + audio) suggests a separate consumer-facing gallery/experience page.
   - Interesting product angles: zero-install file/data transfer, offline capability, privacy (QR = no account, no server in the middle).
2. **vibeos** — a custom x86 OS with a user-app SDK (callbacks, windows, drawing, keyboard/mouse). This is a systems playground/portfolio piece. The SDK guide being in Italian hints at a personal/educational angle (bootstrapped for learning or for Italian-speaking friends).

## Product thinking rules for these projects
1. **For fountain (consumer/utility web)**
   - Solvability first: does the flow work in <3 steps, in under 30 seconds, on a phone camera?
   - Perfect scan reliability beats features. A version where scanning fails = product failure.
   - Offline/accountless is a feature: keep the server out of the flow where possible.
   - The receiver side must not assume a desktop; design for a phone-to-phone reality.
2. **For vibeos (developer/systems product)**
   - The SDK is the product: developer experience (callbacks, window lifecycle, painting) is what makes or breaks it.
   - Demo-ability: a calculator app is fine, but a demo app that showcases graphics/physics/multitasking sells the OS.
   - Compatibility guardrails: improving the kernel must not silently break the documented SDK contract (SDK_GUIDE.md).
3. Whenever the user asks "should we build X?" — give a recommendation with reasoning, don't just list options. They want opinions from a product person, not a menu.

## Suggested roadmap thinking (at the right altitude)
- fountain: (1) make round-trip scan rock solid → (2) one killer scenario demoed end-to-end → (3) then new capabilities. Test via test-roundtrip.mjs + Playwright + real camera (controlmcp on Safari/Chrome).
- vibeos: keep kernel stable while growing the SDK surface. Each SDK addition should come with a demo app. The OS is the demo of the SDK's power.

## How to talk about products with this user
- Direct, opinionated, no buzzwords ("synergy", "paradigm" → banned).
- Concrete tradeoffs over abstract principles. Tie every idea back to "who uses it and when".
- They like building things that are real and work — demos, running code, visible progress — over forecasts and decks.