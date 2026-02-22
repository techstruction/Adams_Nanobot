"""Apple Notes skill module"""

from .notes_manager import (
    list_notes,
    read_note,
    search_notes,
    create_note,
    add_to_note,
    notes_manager
)

# Convenience exports
__all__ = [
    'list_notes',
    'read_note',
    'search_notes',
    'create_note',
    'add_to_note',
    'notes_manager'
]
