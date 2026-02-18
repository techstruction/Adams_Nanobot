# UPDATE_LEDGER.md

Track all changes, updates, skills added, and configuration changes here.

---

## [2026-02-18] — Initial MVP Setup

### Environment
- Installed Python 3.12 (via Homebrew) and `uv` for dependency management.
- Cloned `HKUDS/nanobot` repository and installed in editable mode (`uv pip install -e .`).
- Ran `nanobot onboard` to initialize `~/.nanobot/config.json`.

### Model Configuration
- Configured **Nvidia NIM** as the LLM provider via the `openai` provider block.
  - `apiBase`: `https://integrate.api.nvidia.com/v1`
  - Model: `openai/moonshotai/kimi-k2.5-instant` (instant/non-reasoning mode)
- Configured **Brave Search** for real-time internet access.

### Channels
- Enabled **Telegram** channel (`@Adams_Tech_ClawdBot`) in `config.json`.
- Verified `nanobot gateway` starts successfully with Telegram polling active.

### Skills Added
- **`telegram_notify`** (`nanobot/skills/telegram_notify/`)
  - `SKILL.md`: Skill definition for sending proactive Telegram messages.
  - `notify.py`: Helper script that reads token from `config.json` and sends a message to a given chat ID.

---

## [2026-02-18] — Kimi k2.5 Instant Mode Optimization

### Problem
- Default Kimi k2.5 response time was ~32 seconds due to internal "thinking" (reasoning) mode being enabled by default.

### Solution
- Added `model_overrides` to the `openai` provider spec in `nanobot/providers/registry.py`:
  - `kimi-k2.5-instant` → sends `extra_body: {thinking: {type: disabled}}` to disable reasoning, reducing latency to ~3s.
  - `kimi-k2.5` → keeps `temperature: 1.0` as required by the API.
- Updated `~/.nanobot/config.json` default model to `openai/moonshotai/kimi-k2.5-instant`.

### Bug Fix
- Fixed model resolution conflict: the `openai/` prefix was bypassing provider-specific overrides. Added `openai/` to `skip_prefixes` in the `moonshot` provider spec.
- Added `loguru` import to `litellm_provider.py` (was missing).
- Switched project to **editable install** (`uv pip install -e .`) so local source changes take effect immediately without reinstalling.

---

## Files Modified
| File | Change |
|------|--------|
| `~/.nanobot/config.json` | API keys, model, Telegram token |
| `nanobot/providers/registry.py` | Kimi instant mode overrides, skip_prefixes fix |
| `nanobot/providers/litellm_provider.py` | Added loguru import |
| `nanobot/skills/telegram_notify/SKILL.md` | New skill |
| `nanobot/skills/telegram_notify/notify.py` | New skill helper |
| `PRODUCT_LEDGER.md` | Project documentation |
| `UPDATE_LEDGER.md` | This file |
