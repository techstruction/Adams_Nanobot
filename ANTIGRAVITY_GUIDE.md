# How to Use the Antigravity Skill

The **Antigravity Skill** is a meta-level orchestration layer for NanoClaw. It allows the agent to switch into a "Senior Staff Engineer" persona and delegate complex, multi-step development tasks to autonomous background sub-agents.

## 🚀 Getting Started

To trigger Antigravity, simply use the word **"Antigravity"** in your request. This tells NanoClaw to stop being a general assistant and start being an expert coder.

### The Persona
When in Antigravity mode, the agent:
- Writes **production-ready, optimized code**.
- Follows the **3-layer architecture** (Directive, Orchestration, Execution).
- Is **proactive** in finding and fixing bugs, typos, and technical debt.
- Prefers **token-efficient** implementations.

---

## 🛠 Sample Commands

### 1. Skill Auditing & Improvement
Use these to keep your NanoClaw sharp and up-to-date.

- **"Antigravity: Audit all my local skills and fix any broken links or missing descriptions in the SKILL.md files."**
- **"Use your Antigravity skill to analyze the `weather` skill and add air quality support if the API allows it."**
- **"Antigravity, review `nanobot/agent/loop.py` and suggest 3 ways to optimize the message processing latency."**

### 2. Autonomous Skill Creation
Instead of micro-managing file creation, let Antigravity handle the research and scaffolding.

- **"Antigravity: Create a new skill called `github-stats` that can pull my repository metrics and summarize them."**
- **"Use Antigravity to build a `system-monitor` skill for macOS that alerts me if CPU usage stays above 90%."**
- **"Antigravity: I want a skill that integrates with JIRA. Design the `SKILL.md` and the core Python scripts for me."**

### 3. Deep Refactoring
Ideal for long-running tasks that you don't want to wait for in the main chat.

- **"Antigravity: Refactor the `dashboard` skill to use a more modular Python backend instead of just one large `server.py`."**
- **"Use Antigravity to migrate my local memory storage from JSON to a lightweight SQLite database."**
- **"Antigravity, audit the entire `nanobot/providers/` directory and ensure all providers have consistent error handling."**

### 4. System Maintenance
Keep the infrastructure clean.

- **"Antigravity: Scan the repo for any un-ignored temporary files and update the `.gitignore` accordingly."**
- **"Use Antigravity to document every undocumented function in `nanobot/agent/subagent.py`."**

---

## 📈 Monitoring Antigravity

Since Antigravity often runs in the background using **sub-agents**, you can monitor its progress in two ways:

1. **Terminal Logs**: Check `nanobot_gateway.log` for lines starting with `Subagent [TASK_ID]`.
2. **History**: Antigravity is instructed to log its major actions in `memory/HISTORY.md` or `UPDATE_LEDGER.md`.

## ⚠️ Pro-Tips

- **Be Technical**: Antigravity understands engineering jargon. You can talk about "singletons," "concurrency," "decorators," and "RESTful patterns."
- **Autonomy**: You don't need to tell it which files to edit; simply describe the goal (e.g., "Implement X") and it will find the relevant files.
- **Verification**: Always ask it to "Verify your work" if you want it to run the code or triggered a test after modification.

---

*Version: 1.0.0*
*Codename: NanoClaw Ascend*
