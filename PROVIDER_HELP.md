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

## Fast recommendation for tired humans
If the user just wants the quickest likely path to a working Starship brain, recommend this order:
1. **ChatGPT 5.4 API** if they are okay with API billing and want the most straightforward copy-paste setup
2. **Gemini API** if they prefer Google or already use AI Studio
3. **ChatGPT Codex (OAuth)** if they specifically want ChatGPT-style account reuse and are okay with a more human-in-the-loop first login

Say this plainly:
- **API paths** usually mean "create key, paste key, done"
- **OAuth path** usually means "do a real human login once, then reuse it later"
- a normal ChatGPT subscription does **not** automatically mean OpenAI API access is already enabled

## How Starship currently detects readiness
The current onboarding and launch flow checks for provider readiness in these places:
1. live environment variables such as `OPENAI_API_KEY`, `GEMINI_API_KEY`, and `GOOGLE_API_KEY`
2. OpenClaw config env vars in `~/.openclaw/openclaw.json`
3. Starship's saved credentials file at `var/provider_credentials.json` (in this repo that means `git/repositories/starship/var/provider_credentials.json`)
4. Docker container env for the running `openclaw-starship` container when present
5. a reusable Codex auth file such as `~/.codex/auth.json`

That means the Starship should tell the user exactly **which source** it found, not just say "ready" in a vague way.

If a user says "I already pasted the key, where did it go?", check the saved credentials file path first before assuming the paste failed.

## What green, yellow, and red should mean
- **Green**: Starship found a usable credential or reusable auth profile and can launch that provider now.
- **Yellow**: the user started setup or pasted something, but a human step or persistence/verification step is still incomplete.
- **Red**: Starship cannot currently find a usable credential or auth profile for that provider.

## Provider-by-provider concierge guidance

### ChatGPT Codex (OAuth)

**When to recommend it first**
- The user wants ChatGPT-style account reuse instead of juggling API keys.
- The user is comfortable doing a real browser login and any MFA step.
- The user wants a path that may feel more natural after the first setup.

**When not to recommend it first**
- The user is remote/headless and hates auth friction.
- The user wants the fastest possible "copy one secret and go" setup.
- The user wants a path that is easiest to explain in one short message.

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
3. Continue into the Codex setup panel and read the built-in instructions.
4. Open the official Codex auth docs or login flow in a browser using the intended OpenAI account.
5. Complete any requested MFA, text code, email confirmation, or approval step.
6. If the setup is remote/headless or the normal browser flow is awkward, use the documented device-code or trusted-machine auth path.
7. Return to Starship once reusable local Codex auth state exists on the machine.
8. Check the readiness panel. It should turn **green** only after a reusable Codex auth file or equivalent reusable local auth state is actually detected.

**What can be automated**
- Detecting an already-valid stored auth file or equivalent reusable local auth state
- Reusing cached auth on later runs
- Routing the user back into onboarding with clear readiness state
- Explaining the right human steps in the onboarding UI

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
- If browser-driven login is awkward, offer or recommend device-code or trusted-machine auth instead of pretending callback capture is guaranteed.
- If the user is remote/headless, prefer device-code over brittle callback expectations.
- If verification just changed, have the user fully complete the provider-side verification flow before retrying.
- If a trusted-machine auth file is reused, verify the copied auth state is intact and securely handled.
- If the panel stays red after a supposedly successful login, check whether `~/.codex/auth.json` or the equivalent local Codex auth state actually exists and is readable instead of assuming success.

**Readiness signs the Starship should surface**
- Green: reusable Codex auth file or equivalent local auth state detected.
- Yellow: login flow started or partial progress exists, but human completion is still needed.
- Red: no usable Codex auth path is configured yet.

**Date last reviewed:** 2026-04-24

### ChatGPT 5.4 API

**When to recommend it first**
- The user wants the simplest likely setup.
- The user is okay with API billing.
- The user wants a clear key-based path that works well in local and remote environments.

**When not to recommend it first**
- The user refuses API billing.
- The user specifically wants browser-account reuse instead of keys.

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
10. Confirm the readiness panel turns **green** and that Starship says it found `OPENAI_API_KEY`, whether from env/config or the saved `var/provider_credentials.json` file.

**What can be automated**
- Detecting whether `OPENAI_API_KEY` is already present
- Saving a pasted key into `var/provider_credentials.json` for later local reuse
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
- If the user pasted a key and the panel still is not green, check whether the key was actually persisted to `var/provider_credentials.json` or exported into the runtime env.

**Readiness signs the Starship should surface**
- Green: usable OpenAI API key detected.
- Yellow: key was entered or partial setup exists, but readiness is not confirmed yet.
- Red: no usable OpenAI API key is configured yet.

**Date last reviewed:** 2026-04-24

### Gemini API

**When to recommend it first**
- The user already has a Google account handy.
- The user prefers Google's tooling or wants a second provider ready.
- OpenAI setup is blocked and a fast alternate API-key path is helpful.

**When not to recommend it first**
- The user is confused by multiple Google accounts and account switching is likely to trip them up.
- AI Studio access is not yet enabled and the user wants the fewest possible external steps.

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
10. Confirm the readiness panel turns **green** and says whether it found `GEMINI_API_KEY` or `GOOGLE_API_KEY`.

**What can be automated**
- Detecting whether `GEMINI_API_KEY` or `GOOGLE_API_KEY` is already present
- Saving a pasted key into `var/provider_credentials.json` for later local reuse
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
- If the key was pasted but readiness stays red, check whether the saved credentials file or runtime env actually contains the Gemini key.

**Readiness signs the Starship should surface**
- Green: usable Gemini API key detected.
- Yellow: key was entered or partial setup exists, but readiness is not confirmed yet.
- Red: no usable Gemini API key is configured yet.

**Date last reviewed:** 2026-04-24

## Support script the Starship should follow
When helping a user live, the Starship should usually say:
1. which provider it recommends first, and why
2. the exact website to open
3. the exact credential or login step the provider will likely ask for
4. exactly what to paste back into Starship, if anything
5. what green/yellow/red means on the readiness panel
6. what to do next if the panel does not turn green

## See also
- `docs/quickstart_onboarding.md`
- `docs/codex_oauth_setup_research.md`

## Future use
This document should eventually be structured so parts of it can be fed into other AIs as a temporary knowledge base for helping users connect providers to the Starship.
