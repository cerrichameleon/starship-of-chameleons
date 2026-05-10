# Codex OAuth Setup Research

## High-confidence findings

### Can ChatGPT Codex OAuth be set up without human intervention?
Short answer: **not reliably, and generally no for a clean first-time setup**.

Why:
- OpenAI Codex OAuth uses a browser-based OAuth flow with PKCE.
- The documented flow requires opening an authorization page at `https://auth.openai.com/oauth/authorize?...`.
- A human may need to log in, confirm account access, and potentially complete verification or security steps.
- OpenClaw documentation explicitly describes a human-facing browser login plus either callback capture or pasting back the redirect URL/code.
- OpenAI Help documentation for some account/org capabilities also references real-world identity verification steps such as government ID and account/email confirmation. Those are inherently human steps.

Conclusion:
- **Full unattended first-time setup should not be assumed possible.**
- The Starship should treat first-time Codex OAuth as a guided human setup step.
- After successful login, refresh can often be handled automatically by stored tokens.

## What appears automatable
- Generating PKCE verifier/challenge and OAuth state.
- Opening the correct authorization URL.
- Listening for a local callback URL such as `http://127.0.0.1:1455/auth/callback`.
- Exchanging the returned code at the token endpoint.
- Storing access token, refresh token, expiry, and account identity.
- Refreshing expired credentials automatically later.

## What likely still requires a human
- Visiting the OpenAI authorization page.
- Logging in to the OpenAI/ChatGPT account.
- Approving access if prompted.
- Handling SMS/email/2FA/security checks if OpenAI requests them.
- Handling any identity or organization verification requirements.
- Copy-pasting the callback URL/code manually if automatic callback capture fails.

## Source-backed flow shape
Based on OpenClaw OAuth docs, the Codex OAuth flow is:
1. Generate PKCE verifier/challenge and random state.
2. Open the authorization URL.
3. Try to capture callback on `http://127.0.0.1:1455/auth/callback`.
4. If callback capture fails, ask the user to paste the redirect URL or code.
5. Exchange the code at `https://auth.openai.com/oauth/token`.
6. Store `{ access, refresh, expires, accountId }`.

## Product implication for Starship
Starship should support two layers:

### 1. Automated setup assistance
The onboarding page should:
- explain what Codex OAuth is
- open the correct auth page
- try to capture the callback automatically
- clearly tell the user what step is human-required
- fall back to a manual paste-code step when necessary

### 2. QuickStart guidance for unavoidable human steps
The onboarding page should contain a dedicated guided section for Codex OAuth setup.

Suggested user-facing guidance:
1. Create or sign in to your OpenAI / ChatGPT account.
2. Be ready to complete any required email, phone, 2FA, or account verification step.
3. Click **Connect Codex OAuth**.
4. Your browser opens the OpenAI authorization page.
5. Sign in and approve access.
6. If the Starship detects the callback automatically, setup continues.
7. If not, copy the final redirected URL or authorization code and paste it back into the Starship onboarding field.
8. Starship exchanges the code, stores the token set, and confirms success.
9. After that, token refresh should usually happen automatically.

## URLs the onboarding should reference
- OpenAI developer/platform home: `https://platform.openai.com/`
- OpenAI auth endpoint family: `https://auth.openai.com/`
- Organization verification info: `https://help.openai.com/en/articles/10910291-api-organization-verification`

## Recommendation
- Do **not** design the Starship around the assumption that Codex OAuth can be completed fully hands-free.
- Do design the Starship onboarding so the human-required steps are few, explicit, guided, and easy.
- Make Codex OAuth one supported path among several, not the only way to bring a brain online.
