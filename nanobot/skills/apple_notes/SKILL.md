# Apple Notes Skill

Complete Apple Notes integration for nanobot - List, read, search, create, and append to notes.

## Features

- **List Notes**: Get all notes with titles and metadata
- **Read Note**: Read full content of any note by title
- **Search Notes**: Search across all notes by keyword
- **Create Note**: Create new notes with custom content
- **Append to Note**: Add content to existing notes
- **Delete Note**: Remove notes (with confirmation)

## Requirements

- macOS with Apple Notes.app
- Python 3.12+
- AppleScript support (built-in on macOS)
- iCloud account (optional but recommended)

## Installation

The skill is automatically loaded by nanobot when placed in the skills directory.

## Usage

### List All Notes

```bash
# Get all note titles
nanobot agent -m "List all my Apple Notes"

# Get notes with metadata
nanobot agent -m "Show me all my notes with creation dates"
```

### Read Note by Title

```bash
# Read a specific note
nanobot agent -m "Read my note titled 'Shopping List'"
```

### Search Notes

```bash
# Search for keyword in all notes
nanobot agent -m "Search my notes for 'configuration'"

# Case-insensitive search
nanobot agent -m "Find notes containing 'NVIDIA'"
```

### Create New Note

```bash
# Create a new note
nanobot agent -m "Create a new note titled 'Meeting Notes' with content 'Discuss Q1 planning'"

# Create note in specific folder
nanobot agent -m "Create note 'Ideas' in folder 'Project X'"
```

### Append to Existing Note

```bash
# Add to existing note
nanobot agent -m "Add to my note 'Meeting Notes': Action items - Follow up with team"
```

### Delete Note

```bash
# Delete note (will confirm)
nanobot agent -m "Delete note 'Old todo list'"
```

## API

### Functions

#### list_notes()
Returns list of all notes with metadata

#### read_note(title)
Returns content of note with matching title

#### search_notes(keyword)
Returns list of notes containing keyword

#### create_note(title, body, folder="Notes")
Creates new note with title and content

#### append_to_note(title, append_text)
Appends text to existing note

#### delete_note(title)
Deletes note (with confirmation)

## Technical Details

### AppleScript Integration

Uses macOS native AppleScript to interact with Notes.app:

```applescript
tell application "Notes"
    set allNotes to every note
    return name of allNotes
end tell
```

### Notes Structure

Each note contains:
- `name`: Note title
- `body`: Note content
- `id`: Unique identifier
- `creation_date`: Creation timestamp
- `modification_date`: Last modified timestamp
- `folder`: Folder containing the note

## Limitations

- Notes must have unique titles (skill uses title to identify notes)
- Cannot access password-protected notes
- iCloud sync required to see notes across devices
- Maximum note size: ~1MB

## Data Safety

- Read-only operations are safe
- Create/append operations modify your actual notes
- Delete operation is destructive (confirmation required)

## Troubleshooting

**"Notes got an error: AppleEvent timed out"**
- Notes.app may not be responding
- Try quitting and reopening Notes.app

**"Note not found"**
- Use quote marks around titles with spaces
- Check capitalization

## Examples

### Create a log note
```
Create note titled 'Command Log' with today's date and list of commands I ran
```

### Append to daily journal
```
Append to note 'Journal 2026-02-21': Had a productive coding session today
```

### Search for project notes
```
Find all notes containing 'nanobot' and 'dashboard'
```

## Performance

- List operations: < 1 second for 100 notes
- Search: < 2 seconds for 1000 notes
- Create/Append: < 1 second

---

**Version:** 1.0.0  
**Status:** Production Ready  
**macOS Compatibility:** 10.15+
