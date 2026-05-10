# Starship QuickStart Onboarding

This page is for real humans, especially tired or busy ones.

The goal is simple:
- pick a brain path
- get the needed account or credentials
- connect it to the Starship
- launch

If a step must be done by a human because of security, we say so plainly.
We do not send you in circles.

---

# Before you begin

You need:
- a computer with the Starship files downloaded
- internet access
- a browser
- enough time to log in and copy one credential if needed

You do **not** need to understand developer jargon.

---

# Brain Path 1: ChatGPT Codex (OAuth)

## What this path is
This uses your ChatGPT / OpenAI account through Codex login instead of a plain API key.

## Important truth first
This path is **not usually fully hands-free the first time**.
A human normally has to complete the first login.
After that, the login can often be reused and refreshed automatically.

## What OpenAI says officially
OpenAI's Codex docs say:
- Codex supports **Sign in with ChatGPT** and **Sign in with an API key**
- browser login is the default when no valid session exists
- cached login details are reused later
- Codex stores cached login details locally in `~/.codex/auth.json` or the OS credential store
- active ChatGPT sessions usually refresh automatically before expiry
- for headless or remote environments, device code auth is preferred when browser callback flow is awkward
- for CI/CD and trusted automation, the supported advanced pattern is to create `auth.json` once on a trusted machine, then reuse and persist it between runs

## What may be required by OpenAI
Depending on your account state, OpenAI may ask you to:
- sign in with email and password
- use your social login provider
- complete email confirmation
- complete text-message verification or another verification code step
- complete MFA / 2FA
- complete account or organization verification

OpenAI explicitly recommends MFA for Codex-related access.

## Websites to start from
- OpenAI Codex auth docs: `https://developers.openai.com/codex/auth`
- OpenAI Codex CI/CD auth docs: `https://developers.openai.com/codex/auth/ci-cd-auth`
- OpenAI platform: `https://platform.openai.com/`
- OpenAI auth/login family: `https://auth.openai.com/`

## ELI5 setup steps
1. In the Starship onboarding screen, choose **ChatGPT Codex (OAuth)**.
2. Continue into the Codex setup panel.
3. Read the built-in instructions there. Right now this path is mainly a guided walkthrough, not a one-click fully automated login button inside the Starship UI.
4. Open the OpenAI Codex auth page in your browser: `https://developers.openai.com/codex/auth`
5. Sign in with the OpenAI account you want to use for Codex.
6. If OpenAI asks for a password, email code, text code, MFA code, or approval, do that step.
7. If you are using a headless or awkward remote setup, prefer the documented device-code / trusted-machine flow from OpenAI's Codex docs.
8. Return to the Starship and continue once the reusable local Codex auth state exists on the machine.
9. The readiness panel should only turn green after the Starship can actually detect reusable local Codex auth state, such as `~/.codex/auth.json`.

## Trusted reuse / advanced automation
OpenAI's own Codex guidance says a trusted machine can:
1. run the Codex login once
2. create `~/.codex/auth.json`
3. reuse that file on a trusted machine or runner
4. let Codex refresh it automatically later

That means the likely Starship product path is:
- one-time human auth
- then reuse cached auth automatically after that

## What the Starship should say clearly
- this path uses ChatGPT-managed login, not a plain API key
- first-time login may require a human
- the current onboarding UI is honest guidance first, not yet a full in-app OAuth automation flow
- later refresh may be automatic once reusable auth state exists
- device-code flow may be better for remote/headless setups
- cached auth data is sensitive and must be treated like a password

## If something goes wrong
- make sure you are logged into the right OpenAI account
- try again in a normal browser window, not a highly restricted private session
- if OpenAI says MFA is required, finish MFA first
- if browser-driven login is awkward, use the **device code** or trusted-machine auth flow from the Codex docs
- do not assume the current Starship UI will complete the whole OAuth dance for you yet; verify that reusable local Codex auth state actually exists afterward
- if cached auth is being reused on another trusted machine, make sure the auth file was copied securely and not corrupted

---

# Brain Path 2: ChatGPT 5.4 API

## What this path is
This uses OpenAI's normal developer API with an API key.

## Important truth first
This is usually easier to wire up than OAuth, but it may cost money based on usage.

## Website to start from
- OpenAI platform: `https://platform.openai.com/`

## ELI5 setup steps
1. Open `https://platform.openai.com/`.
2. Sign in to your OpenAI account.
3. Make sure you are in the correct organization or personal workspace if OpenAI shows more than one.
4. Go to the API or developer area of the site.
5. Find the section for **API keys**.
6. Click **Create new secret key** or the equivalent button.
7. Give the key a name you will recognize later, for example `Starship Captain`.
8. Copy the key immediately and save it somewhere safe for the moment.
9. Return to the Starship onboarding page.
10. Choose **ChatGPT 5.4 API**.
11. Paste the API key into the Starship input box.
12. Save the configuration.
13. Look at the Starship readiness state. It should move toward green and explain what is still missing if the provider is not actually ready yet.

## Possible extra OpenAI steps
Depending on your account, OpenAI may also require:
- billing setup
- organization verification for some advanced capabilities
- making sure you generated a **new** API key after a verification change

## What the Starship should say clearly
- this path uses an API key
- this path is usually token-billed
- the user owns the provider account and billing relationship

## If something goes wrong
- confirm the key was copied fully
- confirm you are using a valid OpenAI API key, not a chat session token
- if OpenAI says your organization is not verified, follow the verification flow on their site
- if verification just completed, create a **new** API key and try that one

---

# Brain Path 3: Gemini API

## What this path is
This uses Google's Gemini developer/API path.

## Important truth first
This path usually uses a Google account plus an API key.

## Website to start from
- Google AI Studio: `https://aistudio.google.com/`

## ELI5 setup steps
1. Open `https://aistudio.google.com/`.
2. Sign in with the Google account you want to use.
3. Accept any terms or prompts Google shows you.
4. Find the area for getting an API key.
5. Create a Gemini API key.
6. Copy the key immediately.
7. Go back to the Starship onboarding page.
8. Choose **Gemini API**.
9. Paste the API key into the Starship input box.
10. Save the configuration.
11. Look at the Starship readiness state. It should move toward green and explain what is still missing if the provider is not actually ready yet.

## Possible extra Google steps
Depending on account state, Google may ask you to:
- confirm account access
- verify phone/email
- accept terms for AI Studio or developer usage
- enable the relevant project/service before key creation

## What the Starship should say clearly
- this path uses a Google/Gemini API key
- this may be token-billed or quota-limited depending on the account and plan
- the user owns the provider account and billing relationship

## If something goes wrong
- confirm you are using the Gemini API key, not some unrelated Google credential
- make sure the correct Google account is active
- check whether Google asked you to accept terms or enable service access first

---

# Which path should you pick first?

If you want the simplest likely route:
1. **ChatGPT 5.4 API**
2. **Gemini API**
3. **ChatGPT Codex OAuth**

If you specifically want OAuth-style account reuse and are comfortable with browser login steps:
1. **ChatGPT Codex OAuth**

---

# What cannot be done entirely by automation
The Starship can automate many things, but it should not pretend to control human-world security steps.

A real person may still be required for:
- passwords
- 2FA
- text message codes
- email confirmation links
- government ID or organization verification
- accepting provider terms

That is not failure.
That is reality.
The Starship's job is to make those moments as clear and painless as possible.

---

# What happens after setup?
Once one of these provider paths is connected, the Starship should:
- refresh and show the provider readiness state clearly
- tell you which provider path is active
- tell you whether it is using API-key billing or OAuth
- remember the configuration locally
- let you add more providers later
- follow the selected provider order when more than one ready path exists

---

# Design promise
We do not say:
- go read random docs
- good luck
- figure it out

We say:
- here is the next step
- here is the website
- here is what the provider will probably ask you
- here is what to paste back
- here is how to know you are done
