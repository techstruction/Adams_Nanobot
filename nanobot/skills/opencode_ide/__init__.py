"""OpenCode IDE Tool - Meta skill for self-modification"""

from .file_manager import (
    file_manager,
    create_file,
    read_file,
    modify_file,
    delete_file,
    list_files,
    search_files,
    get_project_structure,
    copy_file,
)

from .git_manager import (
    git_manager,
    git_status,
    git_add,
    git_commit,
    git_push,
    git_pull,
    git_branch,
    git_log,
    git_diff,
)

__all__ = [
    # File operations
    "file_manager",
    "create_file",
    "read_file",
    "modify_file",
    "delete_file",
    "list_files",
    "search_files",
    "get_project_structure",
    "copy_file",
    # Git operations
    "git_manager",
    "git_status",
    "git_add",
    "git_commit",
    "git_push",
    "git_pull",
    "git_branch",
    "git_log",
    "git_diff",
]

# Meta version (this skill modifies itself!)
__version__ = "1.0.0"
__codename__ = "Self-Improving"
