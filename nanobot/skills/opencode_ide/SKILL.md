# OpenCode IDE Tool

Self-modifying IDE integration for nanobot - Write code, manage git, and control the OpenCode editor.

## Overview

This meta-skill gives nanobot direct access to its own codebase, enabling:
- Self-improvement through code modification
- Automated git operations
- File management within workspace
- Project scaffolding
- Code analysis and refactoring

## Features

### 📝 File Operations
- Create new files
- Read file contents
- Modify existing files
- Delete files (with confirmation)
- List directory structure
- File search across workspace

### 🚀 Git Integration
- Git status checking
- Stage files for commit
- Create commits with messages
- Push to remote repositories
- Pull latest changes
- Create and switch branches
- Merge branches

### 🔍 Code Analysis
- List recent file changes
- Check for uncommitted changes
- View commit history
- Get project structure
- Find files by pattern

### 🤖 Self-Modification
- Modify own skill files
- Add new skills dynamically
- Update CLI commands
- Refactor code
- Add comments/documentation

## Usage

### File Management

```bash
# Create a new file
nanobot agent -m "Create file 'new_skill.py' in nanobot/skills/ with basic skill template"

# Read file content
nanobot agent -m "Show me the contents of nanobot/skills/apple_notes/SKILL.md"

# Modify existing file
nanobot agent -m "Add a comment header to nanobot/skills/pdf_manager/pdf_manager.py"

# Search for files
nanobot agent -m "Find all files containing 'TODO' in nanobot/"
```

### Git Operations

```bash
# Check status
nanobot agent -m "What's the git status of this repository?"

# Stage files
nanobot agent -m "Stage all files in nanobot/skills/apple_notes/ for commit"

# Create commit
nanobot agent -m "Create a commit message 'feat: add Apple Notes integration'"

# Push changes
nanobot agent -m "Push current branch to origin"

# Create branch
nanobot agent -m "Create and checkout new branch 'feature/skill-auto-loader'"
```

### Self-Modification

```bash
# Add to existing skill
nanobot agent -m "Append function to nanobot/skills/apple_notes/notes_manager.py"

# Create new skill from template
nanobot agent -m "Create complete weather skill using the template from existing skills"

# Update documentation
nanobot agent -m "Update UPDATE_LEDGER.md with recent changes to dashboard"
```

## Technical Architecture

The skill leverages:
- **Python's built-in file I/O** for file operations
- **GitPython** or `subprocess` for git commands
- **Pathlib** for path manipulation
- **AST module** for code analysis
- **Subprocess** for command execution

## Safety & Guardrails

**⚠️ DANGER ZONE:** This skill can modify nanobot's own code!

**Protections:**
- Confirmation required for destructive actions (delete, overwrite)
- Git as safety net (can always revert changes)
- Workspace sandboxing (can't access files outside ~/.nanobot/)
- Backup creation before major modifications
- Read-only mode available

**Recovery:**
```bash
# If something breaks
1. git status (see what changed)
2. git log (find last working commit)
3. git checkout <commit-hash> (go back to working state)
4. Restart nanobot
```

## API

### File Operations

- `create_file(filepath, content)` - Create new file with content
- `read_file(filepath)` - Read file contents
- `modify_file(filepath, operations)` - Apply modifications
- `delete_file(filepath)` - Delete file (confirm)
- `list_files(pattern)` - Find files matching pattern
- `search_files(directory, pattern)` - Search content across files

### Git Operations

- `git_status()` - Get current repository status
- `git_add(files)` - Stage files for commit
- `git_commit(message)` - Create commit with message
- `git_push(remote, branch)` - Push to remote
- `git_pull(remote, branch)` - Pull latest changes
- `git_branch(name)` - Create/switch branches
- `git_log(limit)` - Get recent commit history

### Project Operations

- `get_project_structure()` - Get directory tree
- `list_recent_changes(hours)` - Find recently modified files
- `create_skill_template(name)` - Generate skill from template
- `update_skill_imports(skill_name)` - Auto-update imports

## Dependencies

- Git (command-line)
- Python 3.12+
- GitPython (optional, for advanced operations)

## Future Enhancements

- [ ] Syntax validation before saving files
- [ ] Automatic README generation
- [ ] Skill dependency checking
- [ ] Automatic testing trigger
- [ ] Live code reloading
- [ ] A/B testing of skill versions

---

**Version:** 1.0.0
**Last Updated:** 2026-02-21
**Status:** Production Ready
**Caution:** MODIFIES OWN CODEBASE
