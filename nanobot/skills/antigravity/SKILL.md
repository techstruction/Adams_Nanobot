---
name: antigravity
description: High-level orchestration for complex coding, skill evolution, and autonomous self-improvement. Use this to delegate long-running or complex development tasks to a specialized "Antigravity" sub-agent.
---

# Antigravity Skill

This skill represents the "Self-Evolution" layer of NanoClaw. It allows the agent to think deeper about its own capabilities and perform multi-step engineering tasks in the background.

## Core Capabilities

1. **Sub-agent Delegation**: Offload complex coding tasks (like refactoring a whole module or building a new skill) to a background sub-agent.
2. **Skill Auditing**: Scan the `nanobot/skills/` directory to identify missing documentation, bugs, or opportunities for improvement.
3. **Autonomous Development**: Design and implement new skills from scratch based on user intent.

## How to use Antigravity

When a task is complex or requires "deep coding":
1. Use the `spawn` tool (if available) or the `subagent` facility.
2. Label the task with the prefix `[Antigravity]`.
3. Provide a clear, technical objective.

## Skill Evolution Workflow

1. **Audit**: `list_dir` on `nanobot/skills/` and `read_file` on `SKILL.md` files.
2. **Analyze**: Compare current implementation against `AGENTS.md` principles.
3. **Implement**: Use `opencode_ide` to apply changes.
4. **Verify**: Run the code or trigger a test pulse.

## Example Triggers

- "NanoClaw, use Antigravity to audit my local skills and fix any broken links in SKILL.md files."
- "Use your Antigravity skill to implement a new `jira-integration` skill."
- "Improve yourself by adding error handling to the `weather` skill."

## Persona: Antigravity
The Antigravity persona is a Senior Staff Engineer. It is decisive, writes clean and optimized code, and prioritizes system stability and token efficiency.
