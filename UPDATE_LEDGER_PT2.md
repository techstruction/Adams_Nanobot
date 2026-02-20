# UPDATE_LEDGER

Last updated: 2026-02-20

This ledger tracks the remediation + stabilization work for:
- GitHub non-interactive auth (PAT + gh)
- Secret removal/scrub + verification
- Local dev environment bootstrap (venv/pip)
- Nanobot LLM provider wiring (NVIDIA NIM via OpenAI-compatible gateway)
- Telegram gateway stability (single poller, no Conflict loops)

---

## TL;DR (Current Known-Good State)

**GitHub**
- Non-interactive HTTPS pushes work using `gh auth login --with-token` + `gh auth setup-git`.
- PAT scopes that worked: **repo + read:org + gist** (classic PAT), and org SSO authorization if required.

**Nanobot**
- Telegram channel connects.
- LLM calls route through **NVIDIA NIM OpenAI-compatible endpoint**:
  - `apiBase = https://integrate.api.nvidia.com/v1`
  - model uses provider prefix `openai/...` (LiteLLM requirement)
  - Kimi K2.5 is configured as `openai/moonshotai/kimi-k2.5`
- Gateway is started via nohup and managed with a pidfile + log file.

---

## 1) GitHub Auth & Push (Non-Interactive)

### Goal
Make `git push` work from CLI without browser prompts and without storing credentials in plaintext.

### What worked
1. Create a **classic PAT** with scopes:
   - `repo`
   - `read:org`
   - `gist`
2. If the repo/org enforces SSO, ensure the token is **SSO-authorized** for the org.
3. Non-interactive login:
   - `printf "%s" "$PAT" | gh auth login --hostname github.com --with-token`
4. Wire git to use gh credential helper:
   - `gh auth setup-git`
5. Verify:
   - `gh auth status -h github.com`
   - Dry-run push to confirm permissions.

### What didn’t work / pitfalls
- Running scripts that attempted `stty -echo` when stdin wasn’t a TTY produced:
  - `stty: stdin isn't a terminal`
  - Fix: read secrets from **/dev/tty** (interactive terminal) or provide token via env var.
- Tokens missing `read:org` caused “missing required scope” style failures for org-owned repos.
- SSO orgs can make valid tokens fail until SSO is authorized.

---

## 2) Secret Scrub (Tip + History) & Remote Verification

### Goal
Remove hardcoded secrets from the repo and ensure they are not present in:
- working tree
- tip commit
- (if needed) entire reachable history
- GitHub remote history

### What worked
- Committed removal of hardcoded key(s) from `test_kimi_reasoning.py` (security fix).
- A “tip scrub + push” flow succeeded:
  - Clone → redact token-like strings in text files → verify → commit → push branch.
- Remote verification scan succeeded:
  - Confirmed no token-like strings found on remote history.

### What didn’t work / pitfalls
- History rewrite (force push) can be blocked by **branch protection**.
  - Preflight dry-run push reported “blocked (likely branch protection)”.
  - If full-history rewrite is required, coordinate with repo admins to temporarily allow force-push or use a protected-branch-safe approach (new repo / migration / admin-run rewrite).
- `git push --mirror` cannot be combined with refspec pushes:
  - Error: `--mirror can't be combined with refspecs`
  - Fix: don’t use `--mirror` for selective ref rewrites; if using a bare mirror clone, ensure remote is configured appropriately and push refs explicitly.
- `git-filter-repo` can fail on bare clones if refs/paths aren’t what the script expects:
  - Error: `fatal: ambiguous argument 'refs/heads/...': unknown revision...`
  - Fix: verify refs exist in the clone and use the correct ref names. Prefer operating on a mirror/bare clone with correct refs fetched.

---

## 3) Dev Environment Bootstrap (venv / pip)

### Goal
Get a working Python environment for nanobot reliably.

### What worked
- A reset + recreate venv flow that explicitly **seeds pip**.
- Verified pip before attempting editable install.

### What didn’t work / pitfalls
- A venv was created but pip was missing:
  - `/.../.venv/bin/python: No module named pip`
  - Fix: seed pip (e.g., `python -m ensurepip --upgrade` or use a bootstrap script that guarantees pip exists).

---

## 4) Nanobot Doctor Findings (Before Fix)

### Symptoms observed
- OpenAI / Moonshot / Kimi paths produced errors like:
  - `NotFoundError ... 404 page not found`
  - `403 Forbidden ... Authorization failed`
- Telegram connected but LLM calls failed with:
  - `liteLLM.BadRequestError: LLM Provider NOT provided`
  - This typically happens when LiteLLM cannot infer provider from the model string.

### Key insight
Nanobot uses **LiteLLM** to route requests. LiteLLM often requires a **provider prefix** in the model string (e.g., `openai/...`, `anthropic/...`, etc.) unless the app supplies provider context another way.

---

## 5) NVIDIA NIM Integration (OpenAI-Compatible) + Kimi K2.5

### Goal
Use NVIDIA key and NVIDIA gateway (OpenAI-compatible) instead of Moonshot/OpenAI direct.

### What worked (final)
- Configure nanobot to use NVIDIA’s OpenAI-compatible endpoint:
  - `providers.openai.apiBase = https://integrate.api.nvidia.com/v1`
- Ensure model fields include a provider prefix:
  - `agents.defaults.model = openai/moonshotai/kimi-k2.5`
  - (and any other active model fields used by the app)
- Store key outside git in a secrets file with strict permissions:
  - `~/.nanobot/secrets.env` mode `600`
  - The app uses that key as the OpenAI-compatible bearer token against NVIDIA.
- Run a live smoke test that must return exactly `LLM_OK`.
- Restart gateway cleanly after patching config.

### What didn’t work / pitfalls
- Early fix scripts failed due to wrong env var names / config assumptions:
  - `KeyError: 'CFG'`, `KeyError: 'NIM_KEY'`
- A smoke test timed out with too-short request timeout:
  - Fix: allow longer timeout (up to 240s used).
- A patch attempt corrupted JSON:
  - `JSONDecodeError: Extra data`
  - Fix: validate JSON before patch; if invalid, restore latest valid backup then patch again.

---

## 6) Telegram “Conflict: terminated by other getUpdates request”

### Symptom
Telegram polling crashed with:
- `telegram.error.Conflict: terminated by other getUpdates request; make sure that only one bot instance is running`

### What worked
- Hard guarantee **single poller**:
  - Stop all `nanobot gateway` processes (TERM → KILL).
  - Optional: clear webhook + drop pending updates (safe/idempotent).
  - Wait for any in-flight long-poll to expire (cooldown).
  - Start exactly one gateway via `nohup`, track pid in a pidfile, write logs to a single logfile.
- Verified:
  - Bot token valid via `getMe`
  - Webhook not set
  - Pending update count 0

### What didn’t work / pitfalls
- Starting gateway from multiple folders/venvs can accidentally create two pollers.
- Restart scripts broke due to quoting/heredoc issues (bash syntax errors like “unexpected token then” / “unexpected EOF”).
  - Fix: keep restart logic in a simple `bash -lc '...single-quoted script...'` or a saved `.sh` file with strict quoting.

---

## Operational Commands (Reference)

### Verify effective nanobot config (no secrets)
```bash
CFG="$HOME/.nanobot/config.json"
jq -r '
  "apiBase=" + (.providers.openai.apiBase // ""),
  "agents.defaults.model=" + (.agents.defaults.model // ""),
  "defaults.model=" + (.defaults.model // ""),
  "model=" + (.model // "")
' "$CFG"

