"""
browser.py — Get open browser tabs and URLs on macOS.

Supports: Safari, Google Chrome, Firefox (limited), Arc.
Uses AppleScript via osascript.

Usage:
    python3 browser.py
"""

import subprocess
import sys


SCRIPTS = {
    "Safari": """
        tell application "Safari"
            set output to {}
            repeat with w in windows
                try
                    repeat with t in tabs of w
                        set end of output to (name of t) & "||" & (URL of t)
                    end repeat
                end try
            end repeat
            return output
        end tell
    """,
    "Google Chrome": """
        tell application "Google Chrome"
            set output to {}
            repeat with w in windows
                try
                    repeat with t in tabs of w
                        set end of output to (title of t) & "||" & (URL of t)
                    end repeat
                end try
            end repeat
            return output
        end tell
    """,
    "Arc": """
        tell application "Arc"
            set output to {}
            repeat with w in windows
                try
                    repeat with t in tabs of w
                        set end of output to (title of t) & "||" & (URL of t)
                    end repeat
                end try
            end repeat
            return output
        end tell
    """,
}


def _is_running(app_name: str) -> bool:
    """Check if an application is currently running."""
    script = f'tell application "System Events" to (name of every process) contains "{app_name}"'
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=5)
    return result.stdout.strip().lower() == "true"


def get_browser_tabs(browser: str | None = None) -> list[dict]:
    """
    Get all open tabs from running browsers.

    Args:
        browser: Specific browser name, or None to check all supported browsers.

    Returns:
        List of dicts: [{browser, title, url}, ...]
    """
    browsers_to_check = [browser] if browser else list(SCRIPTS.keys())
    tabs = []

    for b in browsers_to_check:
        if b not in SCRIPTS:
            continue
        if not _is_running(b):
            continue

        result = subprocess.run(
            ["osascript", "-e", SCRIPTS[b]],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            tabs.append({"browser": b, "error": result.stderr.strip()})
            continue

        raw = result.stdout.strip()
        if not raw:
            continue

        for item in raw.split(", "):
            item = item.strip()
            if "||" in item:
                parts = item.split("||", 1)
                tabs.append({
                    "browser": b,
                    "title": parts[0].strip(),
                    "url": parts[1].strip() if len(parts) > 1 else "",
                })

    return tabs


def get_active_tab() -> dict:
    """Get only the currently active/frontmost browser tab."""
    for browser, script in SCRIPTS.items():
        if not _is_running(browser):
            continue
        # Get just the front window's active tab
        if browser == "Safari":
            script = 'tell application "Safari" to return (name of current tab of front window) & "||" & (URL of current tab of front window)'
        elif browser == "Google Chrome":
            script = 'tell application "Google Chrome" to return (title of active tab of front window) & "||" & (URL of active tab of front window)'
        elif browser == "Arc":
            script = 'tell application "Arc" to return (title of active tab of front window) & "||" & (URL of active tab of front window)'

        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and "||" in result.stdout:
            parts = result.stdout.strip().split("||", 1)
            return {"browser": browser, "title": parts[0].strip(), "url": parts[1].strip()}

    return {"error": "No supported browser is running (Safari, Chrome, Arc)"}


if __name__ == "__main__":
    print("Active browser tab:")
    active = get_active_tab()
    print(f"  {active}")

    print("\nAll open browser tabs:")
    tabs = get_browser_tabs()
    if not tabs:
        print("  No browser tabs found (no supported browser running)")
    for t in tabs:
        if "error" in t:
            print(f"  [{t['browser']}] ERROR: {t['error']}")
        else:
            print(f"  [{t['browser']}] {t['title']}")
            print(f"           {t['url']}")
