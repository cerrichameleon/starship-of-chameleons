# Onboarding Milestone Summary - 2026-04-24

## What is now implemented

### 1. Onboarding-first launch path
- Starship launch now leads with onboarding instead of dropping straight into raw Captain chat.
- `/` is gated into provider setup until the user explicitly chooses provider paths and reaches enough readiness to unlock the Captain console.
- launcher output now includes both the root URL and the explicit onboarding URL.
- browser auto-open targets onboarding directly.

### 2. Canonical launcher correction paths
- the repo includes `install_starship_alias.sh` for a global `starship` launcher
- the repo also includes `install_engage_alias.sh` to create or refresh `/usr/local/bin/engage`
- both launcher paths point at the moved Starship launcher under `workspace/git/repositories/starship`
- the repo README also now says plainly that launch begins with onboarding first, not raw Captain chat

### 3. Provider readiness detection
- onboarding now detects readiness for:
  - ChatGPT Codex OAuth
  - ChatGPT 5.4 API
  - Gemini API
- readiness is surfaced as green / yellow / red state with explanatory detail text.

### 4. Better provider onboarding UX
- users can select more than one provider
- users can choose provider order before setup
- users can stop after the first successful provider hookup or continue through the rest
- onboarding copy now recommends a practical starting order
- setup screens now include clearer blocker guidance around verification, terms, wrong account, or bad credential copy

### 5. Fresh Captain chat after onboarding
- after onboarding unlocks the console, the Captain chat can start fresh instead of inheriting stale bridge chatter from earlier testing.

### 6. Explicit onboarding reset path
- the monitor screen now includes **Start onboarding over**
- reset clears persisted onboarding selection/state back to defaults
- reset also clears Captain chat state so repeat first-run testing starts clean

### 7. Concierge provider logistics guidance
- `PROVIDER_HELP.md` was expanded from a stub into a useful operator-facing logistics reference
- it now includes concrete human steps, automation boundaries, pitfalls, troubleshooting, and readiness expectations for the three current provider paths

## Clean onboarding cluster staging list
To keep the next commit small despite unrelated repo churn, stage this exact file list:

- `README.md`
- `RUN_STARSHIP.md`
- `PROVIDER_HELP.md`
- `run_starship.py`
- `install_starship_alias.sh`
- `install_engage_alias.sh`
- `src/starship_protocol/brain_selection.py`
- `src/starship_protocol/engineering.py`
- `src/starship_protocol/onboarding_ui.py`
- `src/starship_protocol/runtime.py`
- `src/starship_protocol/runtime_manifest.py`
- `src/starship_protocol/web_ui.py`

## Important repo-state note
Most of this onboarding cluster is still new/untracked in the current repo state.
That means commit discipline has to be explicit: stage the exact intended files instead of trusting broad `git add .` behavior.

For repeatable staging, use:
- `docs/onboarding_commit_prep_2026-04-24.sh`

## Still worth polishing next
- continue improving provider onboarding copy and troubleshooting depth
- keep reducing UI ambiguity around which ready provider path will actually drive Captain launch
- if you are ready to package this slice, run `docs/onboarding_commit_prep_2026-04-24.sh`, review the staged diff, and cut the exact small commit for the onboarding cluster
