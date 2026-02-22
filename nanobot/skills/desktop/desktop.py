"""
desktop.py — Main entry point for the Nanobot desktop interaction skill.

Routes commands to the appropriate sub-module:
  screenshot  — capture screen
  windows     — list open windows
  browser     — get browser tabs/URLs
  notes       — interact with macOS Notes

Usage:
    python3 desktop.py screenshot [output_path]
    python3 desktop.py windows
    python3 desktop.py windows frontmost
    python3 desktop.py browser
    python3 desktop.py browser active
    python3 desktop.py notes list
    python3 desktop.py notes read "Title"
    python3 desktop.py notes create "Title" "Body"
    python3 desktop.py notes search "keyword"
"""

import sys
import json
from pathlib import Path

# Allow running from any directory
sys.path.insert(0, str(Path(__file__).parent))

import screenshot as _screenshot
import windows as _windows
import browser as _browser
import notes as _notes


def run(command: str, *args) -> dict | list:
    """Dispatch a desktop command and return structured result."""
    cmd = command.lower()

    if cmd == "screenshot":
        path = args[0] if args else None
        return _screenshot.take_screenshot(output_path=path)

    elif cmd == "screenshot_region":
        if len(args) < 4:
            return {"error": "Usage: screenshot_region top left width height"}
        return _screenshot.screenshot_region(int(args[0]), int(args[1]), int(args[2]), int(args[3]))

    elif cmd == "windows":
        if args and args[0] == "frontmost":
            return _windows.get_frontmost_app()
        return _windows.list_windows()

    elif cmd == "browser":
        if args and args[0] == "active":
            return _browser.get_active_tab()
        browser_name = args[0] if args else None
        return _browser.get_browser_tabs(browser=browser_name)

    elif cmd == "notes":
        sub = args[0] if args else "list"
        if sub == "list":
            return _notes.list_notes()
        elif sub == "folders":
            return _notes.list_folders()
        elif sub == "read" and len(args) > 1:
            return _notes.read_note(args[1])
        elif sub == "create" and len(args) > 2:
            return _notes.create_note(args[1], args[2])
        elif sub == "search" and len(args) > 1:
            return _notes.search_notes(args[1])
        else:
            return {"error": f"Unknown notes sub-command: {sub}"}

    else:
        return {"error": f"Unknown command: {command}. Available: screenshot, windows, browser, notes"}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    command = sys.argv[1]
    args = sys.argv[2:]
    result = run(command, *args)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
