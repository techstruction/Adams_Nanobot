"""
notes.py — Read, list, and create notes in macOS Notes app.

Uses AppleScript via osascript to interact with the Notes application.

Usage:
    python3 notes.py list
    python3 notes.py read "Note Title"
    python3 notes.py create "Title" "Body text"
    python3 notes.py search "keyword"
"""

import subprocess
import sys


def list_notes(folder: str | None = None) -> list[dict]:
    """
    List all notes (optionally filtered by folder).

    Returns:
        List of dicts: [{name, folder, id}, ...]
    """
    if folder:
        script = f"""
        tell application "Notes"
            set output to {{}}
            tell folder "{folder}"
                repeat with n in notes
                    set end of output to (name of n) & "||" & id of n
                end repeat
            end tell
            return output
        end tell
        """
    else:
        script = """
        tell application "Notes"
            set output to {}
            repeat with n in every note
                try
                    set folderName to name of container of n
                on error
                    set folderName to "Unknown"
                end try
                set end of output to (name of n) & "||" & folderName & "||" & id of n
            end repeat
            return output
        end tell
        """

    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=15)
    if result.returncode != 0:
        return [{"error": result.stderr.strip() or "Failed to list notes"}]

    raw = result.stdout.strip()
    if not raw:
        return []

    notes = []
    for item in raw.split(", "):
        item = item.strip()
        if "||" in item:
            parts = item.split("||")
            notes.append({
                "name": parts[0].strip(),
                "folder": parts[1].strip() if len(parts) > 2 else "Notes",
                "id": parts[-1].strip(),
            })
    return notes


def read_note(title: str) -> dict:
    """
    Read the body of a note by title.

    Returns:
        dict with keys: name, body, folder
    """
    script = f"""
    tell application "Notes"
        set matchNote to first note whose name is "{title}"
        set noteBody to body of matchNote
        try
            set folderName to name of container of matchNote
        on error
            set folderName to "Notes"
        end try
        return name of matchNote & "||BODY||" & noteBody & "||FOLDER||" & folderName
    end tell
    """
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=10)
    if result.returncode != 0:
        err = result.stderr.strip()
        if "Can't get" in err or "doesn't exist" in err.lower():
            return {"error": f"Note '{title}' not found"}
        return {"error": err or "Failed to read note"}

    raw = result.stdout.strip()
    if "||BODY||" in raw:
        parts = raw.split("||BODY||", 1)
        name = parts[0].strip()
        rest = parts[1].split("||FOLDER||", 1) if "||FOLDER||" in parts[1] else [parts[1], "Notes"]
        return {"name": name, "body": rest[0].strip(), "folder": rest[1].strip() if len(rest) > 1 else "Notes"}

    return {"error": "Unexpected response format"}


def create_note(title: str, body: str, folder: str = "Notes") -> dict:
    """
    Create a new note in the Notes app.

    Returns:
        dict with keys: name, id, success
    """
    # Escape quotes in body
    safe_body = body.replace('"', '\\"')
    safe_title = title.replace('"', '\\"')

    script = f"""
    tell application "Notes"
        try
            set targetFolder to folder "{folder}"
        on error
            set targetFolder to default account
        end try
        set newNote to make new note at targetFolder with properties {{name:"{safe_title}", body:"{safe_body}"}}
        return id of newNote
    end tell
    """
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=10)
    if result.returncode != 0:
        return {"error": result.stderr.strip() or "Failed to create note", "success": False}

    return {"name": title, "id": result.stdout.strip(), "success": True}


def search_notes(keyword: str) -> list[dict]:
    """
    Search notes by keyword in title or body.

    Returns:
        List of matching notes: [{name, folder, snippet}, ...]
    """
    script = f"""
    tell application "Notes"
        set output to {{}}
        set kw to "{keyword.lower()}"
        repeat with n in every note
            set noteBody to body of n
            set noteName to name of n
            if (noteName contains kw) or (noteBody contains kw) then
                try
                    set folderName to name of container of n
                on error
                    set folderName to "Notes"
                end try
                -- Get first 100 chars of body as snippet
                if length of noteBody > 100 then
                    set snippet to text 1 thru 100 of noteBody
                else
                    set snippet to noteBody
                end if
                set end of output to noteName & "||" & folderName & "||" & snippet
            end if
        end repeat
        return output
    end tell
    """
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=20)
    if result.returncode != 0:
        return [{"error": result.stderr.strip() or "Search failed"}]

    raw = result.stdout.strip()
    if not raw:
        return []

    notes = []
    for item in raw.split(", "):
        if "||" in item:
            parts = item.split("||")
            notes.append({
                "name": parts[0].strip(),
                "folder": parts[1].strip() if len(parts) > 2 else "Notes",
                "snippet": parts[2].strip() if len(parts) > 2 else "",
            })
    return notes


def list_folders() -> list[str]:
    """List all Note folders."""
    script = """
    tell application "Notes"
        return name of every folder
    end tell
    """
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=10)
    if result.returncode != 0:
        return []
    return [f.strip() for f in result.stdout.strip().split(", ") if f.strip()]


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "list":
        print("Notes folders:", list_folders())
        print("\nAll notes:")
        for n in list_notes():
            if "error" in n:
                print(f"  ERROR: {n['error']}")
            else:
                print(f"  [{n['folder']}] {n['name']}")
    elif args[0] == "read" and len(args) > 1:
        note = read_note(args[1])
        if "error" in note:
            print(f"Error: {note['error']}")
        else:
            print(f"Title: {note['name']}")
            print(f"Folder: {note['folder']}")
            print(f"Body:\n{note['body']}")
    elif args[0] == "create" and len(args) > 2:
        result = create_note(args[1], args[2])
        print(result)
    elif args[0] == "search" and len(args) > 1:
        results = search_notes(args[1])
        for r in results:
            if "error" in r:
                print(f"Error: {r['error']}")
            else:
                print(f"  [{r['folder']}] {r['name']}: {r['snippet'][:80]}...")
    else:
        print("Usage: python3 notes.py [list|read <title>|create <title> <body>|search <keyword>]")
