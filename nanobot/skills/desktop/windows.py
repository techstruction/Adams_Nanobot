"""
windows.py — List open windows on macOS.

Uses AppleScript via osascript to enumerate all visible application windows.
Returns app name, window title, and whether the app is frontmost.

Usage:
    python3 windows.py
"""

import subprocess
import json
import sys


APPLESCRIPT = """
set output to {}
tell application "System Events"
    set procs to every process whose background only is false
    repeat with proc in procs
        set appName to name of proc
        set isFront to frontmost of proc
        try
            set wins to every window of proc
            repeat with win in wins
                set winTitle to name of win
                set end of output to appName & "||" & winTitle & "||" & (isFront as string)
            end repeat
        end try
    end repeat
end tell
return output
"""


def list_windows() -> list[dict]:
    """
    List all visible open windows.

    Returns:
        List of dicts: [{app, title, frontmost}, ...]
    """
    try:
        result = subprocess.run(
            ["osascript", "-e", APPLESCRIPT],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            err = result.stderr.strip()
            if "not allowed" in err.lower() or "1002" in err or "assistive" in err.lower():
                return [{"error": "Accessibility permission required. Go to System Settings → Privacy & Security → Accessibility → enable Terminal."}]
            return [{"error": err or "osascript failed"}]

        raw = result.stdout.strip()
        if not raw:
            return []

        windows = []
        # osascript returns comma-separated list items
        for item in raw.split(", "):
            item = item.strip()
            if "||" in item:
                parts = item.split("||")
                if len(parts) >= 2:
                    windows.append({
                        "app": parts[0].strip(),
                        "title": parts[1].strip(),
                        "frontmost": parts[2].strip() == "true" if len(parts) > 2 else False,
                    })
        return windows

    except subprocess.TimeoutExpired:
        return [{"error": "Timed out listing windows"}]
    except Exception as e:
        return [{"error": str(e)}]


def get_frontmost_app() -> dict:
    """Return the currently focused application and window."""
    script = """
    tell application "System Events"
        set fp to first process whose frontmost is true
        set appName to name of fp
        try
            set winTitle to name of front window of fp
        on error
            set winTitle to ""
        end try
        return appName & "||" & winTitle
    end tell
    """
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=5)
    if result.returncode == 0 and "||" in result.stdout:
        parts = result.stdout.strip().split("||")
        return {"app": parts[0].strip(), "title": parts[1].strip() if len(parts) > 1 else ""}
    return {"error": result.stderr.strip() or "Could not get frontmost app"}


if __name__ == "__main__":
    print("Frontmost app:")
    front = get_frontmost_app()
    print(f"  {front}")
    print("\nAll open windows:")
    windows = list_windows()
    for w in windows:
        if "error" in w:
            print(f"  ERROR: {w['error']}")
        else:
            marker = " ◀ (active)" if w.get("frontmost") else ""
            print(f"  [{w['app']}] {w['title']}{marker}")
