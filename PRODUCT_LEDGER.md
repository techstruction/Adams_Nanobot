# PRODUCT_LEDGER.md

## Project Description
Nanobot is an autonomous agent capable of browsing the internet, performing tasks, and self-improving by building its own skills.

## Purpose
Provide a highly flexible, extensible, and autonomous digital assistant that operates locally on macOS, leveraging state-of-the-art LLMs and search tools.

## Full Stack
- **Core Engine**: [HKUDS/nanobot](https://github.com/HKUDS/nanobot) (editable install)
- **LLM**: Nvidia NIM → Moonshot Kimi k2.5 (instant/non-reasoning mode)
- **Search**: Brave Search API
- **Channels**: Telegram (`@Adams_Tech_ClawdBot`)
- **Language**: Python 3.12
- **Package Manager**: `uv`

## Environment
**Single environment — local macOS (ARM64)**
- All development, testing, and live operation runs on this machine.
- No VPS staging or production environments.

## Configuration
- **Config file**: `~/.nanobot/config.json`
- **LLM**: Nvidia NIM API key, model `openai/moonshotai/kimi-k2.5-instant`
- **Search**: Brave Search API key
- **Telegram**: Bot token for `@Adams_Tech_ClawdBot`
- **Git Repo**: [techstruction/Adams_Nanobot](https://github.com/techstruction/Adams_Nanobot.git)

## Skills
| Skill | Description |
|-------|-------------|
| `telegram_notify` | Send proactive messages to a Telegram chat via CLI |
