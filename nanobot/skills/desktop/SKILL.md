# Desktop Interaction Skill

This skill gives you the ability to interact with the macOS desktop environment.

## Capabilities

### 1. Take a Screenshot
Capture the current state of the screen.

```bash
python3 ~/.nanobot/skills/desktop/desktop.py screenshot
# or save to a specific path:
python3 ~/.nanobot/skills/desktop/desktop.py screenshot /path/to/output.png
```

Returns: `{ "path": "...", "width": N, "height": N, "base64": "..." }`

Use the `base64` field to describe what's on screen visually.

### 2. List Open Windows
See all open application windows.

```bash
python3 ~/.nanobot/skills/desktop/desktop.py windows
# Get only the frontmost (active) window:
python3 ~/.nanobot/skills/desktop/desktop.py windows frontmost
```

Returns: `[{ "app": "...", "title": "...", "frontmost": true/false }, ...]`

### 3. Get Browser Tabs & URLs
Read open tabs from Safari, Chrome, or Arc.

```bash
# All open tabs across all browsers:
python3 ~/.nanobot/skills/desktop/desktop.py browser
# Only the currently active tab:
python3 ~/.nanobot/skills/desktop/desktop.py browser active
```

Returns: `[{ "browser": "...", "title": "...", "url": "..." }, ...]`

### 4. Interact with Notes App
Read, list, search, and create notes.

```bash
# List all notes:
python3 ~/.nanobot/skills/desktop/desktop.py notes list
# List folders:
python3 ~/.nanobot/skills/desktop/desktop.py notes folders
# Read a note by title:
python3 ~/.nanobot/skills/desktop/desktop.py notes read "My Note Title"
# Create a new note:
python3 ~/.nanobot/skills/desktop/desktop.py notes create "Title" "Body text here"
# Search notes by keyword:
python3 ~/.nanobot/skills/desktop/desktop.py notes search "keyword"
```

## Required macOS Permissions

Before using this skill, ensure Terminal has these permissions:

1. **Screen Recording** (for screenshots):
   System Settings → Privacy & Security → Screen & System Audio Recording → ✅ Terminal

2. **Accessibility** (for window listing):
   System Settings → Privacy & Security → Accessibility → ✅ Terminal

If you see permission errors, tell the user to grant these in System Settings.

## Example Agent Workflows

**"Take a screenshot and describe what's on screen"**
1. Run `desktop.py screenshot`
2. Use the returned `base64` PNG to visually describe the screen contents.

**"What windows do I have open?"**
1. Run `desktop.py windows`
2. Summarize the list of apps and window titles.

**"What URL is open in my browser?"**
1. Run `desktop.py browser active`
2. Return the title and URL of the active tab.

**"Read my note called Meeting Notes"**
1. Run `desktop.py notes read "Meeting Notes"`
2. Return the note body to the user.

**"Save this to my Notes"**
1. Run `desktop.py notes create "Title" "Content"`
2. Confirm the note was created.
