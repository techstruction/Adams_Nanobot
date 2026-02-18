# PRODUCT_LEDGER.md

## Project Description
Nanobot is an autonomous agent capable of browsing the internet, performing tasks, and self-improving by building its own skills.

## Purpose
The purpose of Nanobot is to provide a highly flexible, extensible, and autonomous digital assistant that can operate across multiple environments (local, staging, production) and leverage state-of-the-art LLMs and search tools.

## Full Stack Description
- **Core Engine**: Based on [HKUDS/nanobot](https://github.com/HKUDS/nanobot).
- **LLM**: Nvidia Kimi k2.5 model.
- **Search**: Brave Browser API.
- **Language**: Python (based on HKUDS/nanobot).
- **Orchestration**: Custom skill-building architecture.

## Environment
1. **Local**: MacOS (ARM64) - Development and testing.
2. **VPS Staging**: Ubuntu/Linux - Pre-production validation.
3. **VPS Production**: Ubuntu/Linux - Live operation.

## Configurations
- **LLM API Key**: Nvidia Kimi k2.5.
- **Search API Key**: Brave Search API.
- **Git Repo**: [techstruction/Adams_Nanobot](https://github.com/techstruction/Adams_Nanobot.git).
