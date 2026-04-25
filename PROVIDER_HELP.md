# Provider Help

## Purpose
This document is the Starship's concierge-grade provider logistics knowledge base.

It exists so that any user, including an absolute beginner, can be guided from:
- not knowing what provider to use
- to choosing one
- to getting the required subscription, account, API key and/or OAuth setup
- to connecting that provider cleanly to the Starship

## Starship Provider Logistics Mission
The Starship must be provider-agnostic, but it must not be user-agnostic.

That means:
- the user should never be left lost
- the user should never be sent in circles
- the Starship should automate everything it can
- when human-world steps are required, the Starship must provide exact, current, hand-holding instructions
- these instructions must be maintained and reviewed regularly so they do not drift into lies

## Standing responsibilities
For every provider added to the Starship ecosystem, we should eventually document:
- provider/company name
- official website
- what products/plans they offer
- estimated costs or likely pricing ranges
- whether they offer API keys, OAuth, subscriptions, local hosting, or some combination
- what exact human steps are needed to create an account
- what exact human steps are needed to buy/activate the needed tier
- how to generate credentials
- how to connect those credentials to the Starship
- what can be automated
- what cannot be automated
- common pitfalls
- troubleshooting guidance
- date last reviewed

## Concierge standard
We are the noob angels.

We love noobs.

We do not allow users to feel lost, bounced around, or trapped in vague instructions.

If the Starship cannot do a step itself, it should still be able to guide the user through the step with pinpoint accuracy.

## Current covered paths
- ChatGPT Codex (OAuth)
- ChatGPT 5.4 API
- Gemini API

## Provider-by-provider concierge guidance

### ChatGPT Codex (OAuth)

**Provider/company:** OpenAI  
**Official starting points:**
- https://developers.openai.com/codex/auth
- https://developers.openai.com/codex/auth/ci-cd-auth
- https://platform.openai.com/

**What this path is**
- Uses ChatGPT/OpenAI account login rather than a plain API key.
- Best when the user wants ChatGPT-managed account reuse and is comfortable with a one-time human login.

**Likely account/setup prerequisites**
- Valid OpenAI/ChatGPT account
- Ability to complete email/password, social login, MFA, or verification if OpenAI asks
- Browser access, or device-code fallback for remote/headless setups

**What exact human steps are usually needed**
1. Open the Starship onboarding flow.
2. Choose **ChatGPT Codex (OAuth)**.
3. Start the Codex login flow.
4. Complete OpenAI login in the browser using the intended account.
5. Complete any requested MFA, text code, email confirmation, or approval step.
6. Let the Starship capture the callback, or use device-code/paste-back fallback if callback capture is awkward.
7. Wait for the Starship to confirm the Codex profile is connected.

**What can be automated**
- Opening the login flow
- Detecting an already-valid stored auth profile
- Reusing cached auth on later runs
- Routing the user back into onboarding with clear readiness state

**What cannot be fully automated**
- Password entry
- MFA / 2FA
- email confirmation
- phone/text verification
- account or organization verification required by OpenAI

**Common pitfalls**
- Logging into the wrong OpenAI account
- Browser callback failing on remote/headless setups
- Assuming OAuth is fully hands-free on the first run
- Treating cached auth files as harmless instead of sensitive secrets

**Troubleshooting guidance**
- If callback capture fails, offer or recommend device-code login.
- If the user is remote/headless, prefer device-code over brittle callback expectations.
- If verification just changed, have the user fully complete the provider-side verification flow before retrying.
- If a trusted-machine auth profile is reused, verify the copied auth state is intact and securely handled.

**Readiness signs the Starship should surface**
- Green: Codex OAuth profile detected and reusable.
- Yellow: login flow started or partial progress exists, but human completion is still needed.
- Red: no usable Codex auth path is configured yet.

**Date last reviewed:** 2026-04-24

### ChatGPT 5.4 API

**Provider/company:** OpenAI  
**Official starting point:**
- https://platform.openai.com/

**What this path is**
- Uses OpenAI's normal developer API with an API key.
- Usually the simplest route for users who do not mind API billing.

**Likely account/setup prerequisites**
- OpenAI account
- Access to the correct organization/workspace if more than one exists
- Billing or verification completed if OpenAI requires it for API use

**What exact human steps are usually needed**
1. Sign in at https://platform.openai.com/.
2. Confirm the correct organization or workspace is active.
3. Open the API keys area.
4. Create a new secret key.
5. Copy it immediately.
6. Return to Starship onboarding.
7. Choose **ChatGPT 5.4 API**.
8. Paste the key into the Starship input box.
9. Save and let the Starship verify readiness.

**What can be automated**
- Detecting whether `OPENAI_API_KEY` is already present
- Marking readiness state in onboarding
- Reusing configured API credentials on later runs
- Choosing OpenAI API as a fallback brain path when Codex OAuth is unavailable

**What cannot be fully automated**
- provider-side billing setup
- account verification
- API key creation inside the provider website
- provider terms acceptance

**Common pitfalls**
- Pasting the wrong credential type instead of a real OpenAI API key
- Using the wrong organization/workspace
- Forgetting to create a new key after verification or billing changes
- Expecting chat subscription access to automatically equal API access

**Troubleshooting guidance**
- If the key is rejected, have the user create a fresh key instead of reusing a questionable one.
- If OpenAI mentions organization verification, finish that first and then mint a new key.
- If the user is unsure whether billing is enabled, send them to the platform billing section before retrying.
- Make sure the Starship says plainly that this path is API-key billing, not ChatGPT web login.

**Readiness signs the Starship should surface**
- Green: usable OpenAI API key detected.
- Yellow: key was entered or partial setup exists, but readiness is not confirmed yet.
- Red: no usable OpenAI API key is configured yet.

**Date last reviewed:** 2026-04-24

### Gemini API

**Provider/company:** Google  
**Official starting point:**
- https://aistudio.google.com/

**What this path is**
- Uses Google's Gemini API via API key.
- Good fallback or alternate path when the user prefers Google tooling or already has a Google account ready.

**Likely account/setup prerequisites**
- Google account
- AI Studio access accepted/enabled
- Any required terms, project, or service activation completed

**What exact human steps are usually needed**
1. Sign in at https://aistudio.google.com/.
2. Accept any AI Studio or developer prompts.
3. Find the API key section.
4. Create a Gemini API key.
5. Copy it immediately.
6. Return to Starship onboarding.
7. Choose **Gemini API**.
8. Paste the key into the Starship input box.
9. Save and let the Starship verify readiness.

**What can be automated**
- Detecting whether `GEMINI_API_KEY` or `GOOGLE_API_KEY` is already present
- Marking readiness state in onboarding
- Reusing configured Gemini credentials on later runs
- Falling back to Gemini when stronger-priority providers are absent

**What cannot be fully automated**
- Google account login
- terms acceptance
- account verification prompts
- API key creation on the provider website
- service/project enablement if Google requires it

**Common pitfalls**
- Using the wrong Google account
- Confusing Gemini API keys with unrelated Google credentials
- Skipping AI Studio terms or service enablement steps
- Assuming quota/billing state is already configured correctly

**Troubleshooting guidance**
- If the key fails, confirm the user created a Gemini API key specifically.
- If AI Studio still looks locked down, have the user finish terms acceptance or account checks first.
- If multiple Google accounts are open, verify the intended one is active before regenerating credentials.
- Tell the user clearly whether the Starship found `GEMINI_API_KEY` or `GOOGLE_API_KEY`.

**Readiness signs the Starship should surface**
- Green: usable Gemini API key detected.
- Yellow: key was entered or partial setup exists, but readiness is not confirmed yet.
- Red: no usable Gemini API key is configured yet.

**Date last reviewed:** 2026-04-24

## See also
- `docs/quickstart_onboarding.md`
- `docs/codex_oauth_setup_research.md`

## Future use
This document should eventually be structured so parts of it can be fed into other AIs as a temporary knowledge base for helping users connect providers to the Starship.
