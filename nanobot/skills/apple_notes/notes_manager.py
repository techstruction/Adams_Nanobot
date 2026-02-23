#!/usr/bin/env python3
"""
Apple Notes Manager
Handles all interactions with Apple Notes via AppleScript
"""

import subprocess
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class AppleNotesManager:
    """Manages Apple Notes operations via AppleScript"""

    def __init__(self):
        self.account = "iCloud"  # Default account

    def _clean_note_content(self, content: str) -> str:
        """Clean note content by removing or replacing image references"""
        import re

        # Pattern to match common image file names and extensions
        # This will match patterns like "Screenshot YYYY-MM-DD at HH.MM.SS.png" or "IMG_1234.jpg"
        image_pattern = r"[^\s]*\.(png|jpg|jpeg|gif|bmp|tiff|heic)(?:\s|$)"

        # Remove standalone image filenames (indicated by model error)
        cleaned = re.sub(image_pattern, "[Image]", content, flags=re.IGNORECASE)

        # Also handle the specific pattern mentioned: "Screenshot 2026-02-22 at 10.32.07 AM.png"
        # These often come as quoted filenames
        screenshot_pattern = r'"Screenshot[^"]*\.png"'
        cleaned = re.sub(screenshot_pattern, '"[Screenshot Image]"', cleaned)

        # Additional pattern: Remove orphaned apostrophes/special characters that might remain
        cleaned = re.sub(r'\s+[\'"`]\s+', " ", cleaned)

        return cleaned.strip()

    def _run_applescript(self, script: str) -> str:
        """Execute AppleScript and return output"""
        try:
            result = subprocess.run(
                ["osascript", "-e", script], capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise Exception(f"AppleScript error: {e.stderr}")

    def list_notes(self) -> List[Dict]:
        """List all notes with metadata"""
        script = f"""
        tell application "Notes"
            set allNotes to every note
            set result to ""
            repeat with currentNote in allNotes
                set noteName to name of currentNote
                set noteId to id of currentNote
                set noteBody to plaintext of currentNote
                try
                    set creationDate to creation date of currentNote
                on error
                    set creationDate to "Unknown"
                end try
                set result to result & noteName & "||" & noteId & "||" & noteBody & "||" & creationDate & "
"
            end repeat
            return result
        end tell
        """

        output = self._run_applescript(script)
        notes = []

        for line in output.split("\n"):
            if line.strip():
                parts = line.split("||", 3)
                if len(parts) == 4:
                    # Clean content to remove image references
                    cleaned_content = self._clean_note_content(parts[2])
                    notes.append(
                        {
                            "title": parts[0],
                            "id": parts[1],
                            "content": cleaned_content,
                            "created": parts[3],
                        }
                    )

        return notes

    def read_note(self, title: str) -> Optional[Dict]:
        """Read a specific note by title"""
        script = f'''
        tell application "Notes"
            set targetNote to note "{title}"
            set noteName to name of targetNote
            set noteContent to plaintext of targetNote
            set noteId to id of targetNote
            try
                set creationDate to creation date of targetNote
            on error
                set creationDate to "Unknown"
            end try
            return noteName & "||" & noteContent & "||" & noteId & "||" & creationDate
        end tell
        '''

        try:
            output = self._run_applescript(script)
            parts = output.split("||", 3)
            if len(parts) == 4:
                # Clean content to remove image references
                cleaned_content = self._clean_note_content(parts[1])
                return {
                    "title": parts[0],
                    "content": cleaned_content,
                    "id": parts[2],
                    "created": parts[3],
                }
        except:
            return None

        return None

    def search_notes(self, keyword: str) -> List[Dict]:
        """Search notes containing keyword"""
        all_notes = self.list_notes()
        return [note for note in all_notes if keyword.lower() in note["content"].lower()]

    def create_note(self, title: str, body: str, folder: str = "Notes") -> bool:
        """Create a new note"""
        # Escape quotes in the body
        escaped_body = body.replace('"', '\\"')

        script = f'''
        tell application "Notes"
            set targetFolder to folder "{folder}"
            make new note at targetFolder with properties {{name:"{title}", body:"{escaped_body}"}}
            return "Success"
        end tell
        '''

        try:
            result = self._run_applescript(script)
            return "Success" in result
        except Exception as e:
            print(f"Error creating note: {e}")
            return False

    def append_to_note(self, title: str, append_text: str) -> bool:
        """Append text to existing note"""
        # Escape quotes
        escaped_text = append_text.replace('"', '\\"')

        script = f'''
        tell application "Notes"
            set targetNote to note "{title}"
            set currentBody to body of targetNote
            set newBody to currentBody & "

" & "{escaped_text}"
            set body of targetNote to newBody
            return "Success"
        end tell
        '''

        try:
            result = self._run_applescript(script)
            return "Success" in result
        except Exception as e:
            print(f"Error appending to note: {e}")
            return False

    def delete_note(self, title: str) -> bool:
        """Delete a note (be careful!)"""
        script = f'''
        tell application "Notes"
            set targetNote to note "{title}"
            delete targetNote
            return "Deleted"
        end tell
        '''

        try:
            result = self._run_applescript(script)
            return "Deleted" in result
        except Exception as e:
            print(f"Error deleting note: {e}")
            return False

    def get_note_count(self) -> int:
        """Get total number of notes"""
        script = """
        tell application "Notes"
            return count of notes
        end tell
        """

        try:
            result = self._run_applescript(script)
            return int(result)
        except:
            return 0

    def export_notes(self, output_file: str) -> bool:
        """Export all notes to JSON file"""
        notes = self.list_notes()

        # Convert to serializable format
        export_data = {
            "export_date": datetime.now().isoformat(),
            "note_count": len(notes),
            "notes": notes,
        }

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting notes: {e}")
            return False


# Convenience functions for nanobot
notes_manager = AppleNotesManager()


def list_notes():
    """List all notes (for nanobot integration)"""
    notes = notes_manager.list_notes()
    if notes:
        result = f"Found {len(notes)} notes:\n\n"
        for note in notes:
            result += f"📄 {note['title']}\n"
            result += f"   Created: {note['created']}\n"
            if len(note["content"]) > 100:
                result += f"   Preview: {note['content'][:100]}...\n"
            else:
                result += f"   Preview: {note['content']}\n"
            result += "\n"
        return result
    else:
        return "No notes found."


def read_note(title):
    """Read specific note (for nanobot integration)"""
    note = notes_manager.read_note(title)
    if note:
        result = f"📄 {note['title']}\n"
        result += f"   Created: {note['created']}\n"
        result += f"   Content:\n"
        result += f"   {note['content']}\n"
        return result
    else:
        return f"Note '{title}' not found."


def search_notes(keyword):
    """Search notes (for nanobot integration)"""
    matching_notes = notes_manager.search_notes(keyword)
    if matching_notes:
        result = f"Found {len(matching_notes)} notes matching '{keyword}':\n\n"
        for note in matching_notes:
            result += f"📄 {note['title']}\n"
            lines = note["content"].split("\n")
            for i, line in enumerate(lines[:5]):  # Show first 5 lines
                if keyword.lower() in line.lower():
                    # Highlight the match
                    result += f"   → {line}\n"
            result += "\n"
        return result
    else:
        return f"No notes found matching '{keyword}'."


def create_note(title, body, folder="Notes"):
    """Create new note (for nanobot integration)"""
    if notes_manager.create_note(title, body, folder):
        return f"✅ Note '{title}' created successfully!"
    else:
        return f"❌ Failed to create note '{title}'."


def add_to_note(title, append_text):
    """Append to existing note (for nanobot integration)"""
    if notes_manager.append_to_note(title, append_text):
        return f"✅ Added to note '{title}' successfully!"
    else:
        return f"❌ Failed to add to note '{title}'."
