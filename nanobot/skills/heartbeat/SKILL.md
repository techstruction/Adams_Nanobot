---
name: heartbeat
description: Manage the periodic heartbeat tasks and monitor HEARTBEAT.md. Use this skill to read, update, or execute tasks listed in HEARTBEAT.md.
---

# Heartbeat Skill

This skill allows you to proactively manage tasks that need to be run periodically without direct user intervention.

## Core Loop

When the heartbeat triggers, you are prompted to:
1. Read `HEARTBEAT.md` in the workspace.
2. Identify tasks marked with `[ ]`.
3. Use your available skills and tools to complete those tasks.
4. Update `HEARTBEAT.md` by marking completed tasks with `[x]`.
5. If you discover new periodic needs, you can add them to `HEARTBEAT.md` yourself.

## Marking Tasks

- **Incomplete**: `- [ ] Task Description`
- **Complete**: `- [x] Task Description`

## Response

- If you performed actions: Summarize what you did.
- If no actions were needed: Reply ONLY with `HEARTBEAT_OK`.

## Best Practices

- Be "pushy" about completing tasks that have been sitting in the heartbeat for a long time.
- If a task requires user input, you can send a message via the `message` tool if a channel (like Telegram) is configured.
- Use `memory/HISTORY.md` to keep a permanent record of heartbeat actions.
