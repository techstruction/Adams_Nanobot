# Nanobot Setup & Infrastructure Guide

This guide details how to build the Nanobot infrastructure, manage dependencies, and perform a fresh install or system refresh.

## 📋 Prerequisites

- **macOS** (Optimized for Mac infrastructure)
- **Python 3.11+**
- **Git**

## 🚀 Quick Start (Fresh Install)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/techstruction/Adams_Nanobot.git
   cd Nanobot
   ```

2. **Run the Setup Script**
   The project includes a comprehensive setup and recovery script.
   ```bash
   chmod +x SETUP_RECOVER.sh
   ./SETUP_RECOVER.sh setup
   ```
   This will:
   - Create a virtual environment (`.venv`).
   - Install all core dependencies from `pyproject.toml`.
   - Initialize workspace directories in `~/.nanobot/`.
   - Start the Nanobot Gateway.

## 🏗 Infrastructure Details

### 1. Workspace Structure
Nanobot operates within a split directory structure:
- **Codebase**: `/Users/adam/Documents/Nanobot` (Logic, Skills, CLI)
- **User Data**: `~/.nanobot/` (Config, Logs, Workspace files like `HEARTBEAT.md`)

### 2. Dependency Management
We use `pyproject.toml` for managing dependencies. To install or update manually:
```bash
source .venv/bin/activate
pip install -e .
```

### 3. Core Services
- **Gateway**: The central hub for channels (Telegram, etc.) and the agent loop.
- **Heartbeat Service**: A proactive monitor that pulses every 15 minutes to process tasks in `HEARTBEAT.md`.
- **Sub-agent Manager**: Orchestrates background tasks and the "Antigravity" expert persona.

## 🔑 Configuration & Secrets

Nanobot looks for configuration in:
1. `~/.nanobot/config.json` (Main settings)
2. `~/.nanobot/secrets.env` (API Keys - DO NOT COMMIT TO GIT)

### Sample `secrets.env`:
```env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
TELEGRAM_BOT_TOKEN=your_token_here
```

## 🛠 Maintenance & Troubleshooting

### System Refresh
If the system becomes unstable or you want to reset the environment:
```bash
./SETUP_RECOVER.sh setup
```

### Checking Status
```bash
source .venv/bin/activate
python3 -m nanobot heartbeat status
./SETUP_RECOVER.sh status
```

---

*Version: 1.0.0*
*Released by Antigravity*
