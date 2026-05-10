# Features Next

## Immediate priorities

### 1. QuickStart installer
A first-run setup flow that allows a new user to:
- choose preferred brain/provider options
- enter API keys or auth details once
- save usable local config
- launch the Starship without shell spelunking
- follow a dedicated guided Codex OAuth flow when human login/verification steps are required

### 2. Startup manifest/spec readout
At launch, the Captain should be able to inspect the real current manifest and explain:
- which provider is active
- which fallback order is configured
- whether token-using paths are active
- what the current runtime specs are

The goal is to let the AI speak from real current configuration rather than from hand-written boilerplate.
