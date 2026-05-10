# Starship Blackboard

This file is a working reminder board for the Starship build.
Read it periodically during active development and heartbeat wakes.

## Core build doctrine
- Build a real Starship runtime, not scattered demos pretending to be a Starship.
- The top-level entity is `Starship`, using has-a composition for operations.
- The runtime must survive independently of any face. Rip the face off and it keeps running.
- Follow strict MVVM separation. Model knows nothing about View or ViewModel.
- UI is important, but it is only one interchangeable face over the runtime.

## Captain doctrine
- The Captain should be simple in concept: a Chameleon with strong personality/mission guidance, authority tools, and crew communication access.
- Do not hardcode crew composition. The Captain should assess mission needs, research when needed, draft a proposal, get approval, and then instantiate crew.
- Captain should have access to multiple communication modes and choose lean mission-appropriate structures.

## Communication doctrine
- Internal communication is core architecture, not a side feature.
- Keep at least these three modes available:
  - direct actor-style messaging
  - mailbox / queue-based communication
  - blackboard / shared artifact collaboration
- The Starship is a facilitator and should support different communication patterns for different mission types.
- Software, film, robotics, engineering, and other missions may need different collaboration forms.

## Growth doctrine
- Optimize for dynamism, mutability, and guided morphability more than arbitrary scale.
- Build for lean mission-specific crews, not a bloated city of defaults.
- Keep the architecture extensible toward later capabilities such as directed learning, tool acquisition, perception, and real-world instrumentation.
- Do not pretend those future powers already exist, but do not paint the architecture into a corner.

## Testing doctrine
- Prioritize backend and functional-model unit tests first.
- UI testing is lower priority for now.
- Use tests to prove deterministic behavior and to keep hallucination-like sloppiness out of the core runtime.

## Process doctrine
- Preserve runnable milestones in `Versions/` when they are worth testing.
- Keep reports brief unless a deeper explanation is needed.
- When in doubt, favor real backend progress over cosmetic front-end churn.

## Near-term next features
- QuickStart installer/setup screen: a simple startup flow that lets a user choose provider(s), order them by preference, enter required API keys or auth info once, and get the Starship running without command-line ritual.
- Onboarding-first launch behavior: launcher entrypoints such as `starship` and `engage` should land on onboarding first, not raw Captain chat, until provider selection/setup is complete.
- Provider readiness truth-telling: onboarding and launch should show clear green/yellow/red readiness based on actual detected credentials or auth profiles, and should say which source was found.
- Startup manifest/spec readout: on launch, the Captain should be able to read the real current setup/manifest back to the user instead of being fed fabricated boilerplate, including selected provider order when relevant.
- Provider logistics concierge system: the Starship should maintain current provider-by-provider onboarding knowledge, including pricing estimates, account/signup steps, API key/OAuth setup, local-server options, automatable vs human-required steps, troubleshooting, and precise guidance for newcomers.
