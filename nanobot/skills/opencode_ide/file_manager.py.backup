#!/usr/bin/env python3
"""
OpenCode IDE - File Manager
Handles file operations for nanobot workspace
"""

import os
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Union


class FileManager:
    """Manages file operations within nanobot workspace"""

    def __init__(self, base_path: str = None):
        """Initialize FileManager

        Args:
            base_path: Base directory for file operations
                      (default: ~/.nanobot/workspace/)
        """
        if base_path:
            self.base_path = Path(base_path)
        else:
            self.base_path = Path.home() / ".nanobot" / "workspace"

        self.base_path.mkdir(parents=True, exist_ok=True)

    def create_file(self, filepath: str, content: str) -> Dict[str, Union[bool, str]]:
        """Create a new file with content

        Args:
            filepath: Path relative to base_path or absolute
            content: File content

        Returns:
            Dict with 'success': bool and 'message': str
        """
        full_path = self._resolve_path(filepath)

        # Check if file exists
        if full_path.exists():
            return {
                "success": False,
                "message": f"File already exists: {full_path}",
                "type": "error",
            }

        # Create parent directory if needed
        full_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Write file
            full_path.write_text(content, encoding="utf-8")

            return {
                "success": True,
                "message": f"✅ Created file: {full_path}",
                "type": "created",
                "filepath": str(full_path),
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error creating file: {e}", "type": "error"}

    def read_file(self, filepath: str, preview_lines: int = None) -> Dict[str, Union[str, bool]]:
        """Read file contents

        Args:
            filepath: File to read
            preview_lines: Optional limit to first N lines

        Returns:
            Dict with content and metadata
        """
        full_path = self._resolve_path(filepath)

        if not full_path.exists():
            return {"success": False, "message": f"❌ File not found: {full_path}", "type": "error"}

        try:
            if preview_lines:
                with open(full_path, "r", encoding="utf-8") as f:
                    lines = [next(f) for _ in range(preview_lines)]
                    content = "".join(lines)
            else:
                content = full_path.read_text(encoding="utf-8")

            lines = len(content.split("\n"))
            size = full_path.stat().st_size

            return {
                "success": True,
                "message": f"📄 Preview: {full_path}{{size_str}}{{",
                "type": "content",
                "filepath": str(full_path),
                "lines": lines,
                "size": size,
                "content": content,
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error reading file: {e}", "type": "error"}

    def modify_file(self, filepath: str, operations: Dict) -> Dict[str, Union[bool, str]]:
        """Modify an existing file

        Args:
            filepath: File to modify
            operations: Dict with modification ops:
                - 'append': text to append
                - 'prepend': text to prepend
                - 'replace_line': {'line': num, 'text': new_text}
                - 'find_replace': {'find': str, 'replace': str}

        Returns:
            Success status
        """
        full_path = self._resolve_path(filepath)

        if not full_path.exists():
            return {"success": False, "message": f"❌ File not found: {full_path}", "type": "error"}

        try:
            content = full_path.read_text(encoding="utf-8")
            changed = False
            message_parts = []

            # Append
            if "append" in operations:
                content += f"\n{operations['append']}"
                changed = True
                message_parts.append("appended text")

            # Prepend
            if "prepend" in operations:
                content = f"{operations['prepend']}\n\n{content}"
                changed = True
                message_parts.append("prepended text")

            # Replace line
            if "replace_line" in operations:
                line_op = operations["replace_line"]
                lines = content.split("\n")
                line_num = line_op["line"] - 1

                if 0 <= line_num < len(lines):
                    old_line = lines[line_num]
                    lines[line_num] = line_op["text"]
                    content = "\n".join(lines)
                    changed = True
                    message_parts.append(f"replaced line {line_op['line']}")

            # Find and replace
            if "find_replace" in operations:
                find_replace = operations["find_replace"]
                old_content = content
                content = content.replace(find_replace["find"], find_replace["replace"])
                if content != old_content:
                    changed = True
                    message_parts.append("replaced text")

            if changed:
                # Backup before writing
                backup_path = full_path.with_suffix(f"{full_path.suffix}.backup")
                full_path.rename(backup_path)

                # Write new content
                full_path.write_text(content, encoding="utf-8")

                message = f"✅ Modified {full_path}: {', '.join(message_parts)}"
                message_type = "modified"
            else:
                message = f"ℹ️ No changes made to {full_path}"
                message_type = "info"

            return {
                "success": True,
                "message": message,
                "type": message_type,
                "filepath": str(full_path),
                "changed": changed,
            }

        except Exception as e:
            return {"success": False, "message": f"❌ Error modifying file: {e}", "type": "error"}

    def delete_file(self, filepath: str, confirm: bool = False) -> Dict[str, Union[bool, str]]:
        """Delete a file (confirm by default)

        Args:
            filepath: File to delete
            confirm: Whether confirmation is required

        Returns:
            Success status
        """
        full_path = self._resolve_path(filepath)

        if not full_path.exists():
            return {"success": False, "message": f"❌ File not found: {full_path}", "type": "error"}

        if not confirm:
            return {
                "success": False,
                "message": f"⚠️  Confirm deletion of: {full_path} (set confirm=True)",
                "type": "confirm",
            }

        try:
            # Backup before deletion
            backup_path = full_path.with_suffix(f"{full_path.suffix}.deleted")
            full_path.rename(backup_path)

            return {
                "success": True,
                "message": f"🗑️  Deleted {full_path} (backup: {backup_path})",
                "type": "deleted",
                "filepath": str(full_path),
                "backup": str(backup_path),
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error deleting file: {e}", "type": "error"}

    def list_files(self, pattern: str = "*", directory: str = ".") -> List[str]:
        """List files matching pattern

        Args:
            pattern: Glob pattern (default: '*')
            directory: Subdirectory to search

        Returns:
            List of matching file paths
        """
        search_dir = self.base_path / directory

        if not search_dir.exists():
            return []

        try:
            matches = list(search_dir.rglob(pattern))
            return [str(p) for p in matches if p.is_file()]
        except Exception as e:
            print(f"Error searching: {e}")
            return []

    def search_files(self, pattern: str, content_search: str) -> List[Dict]:
        """Search files by name and content

        Args:
            pattern: Glob pattern for filenames
            content_search: Text to search within files

        Returns:
            List of matching files with line numbers
        """
        files = self.list_files(pattern)
        matches = []

        for filepath in files:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    matching_lines = []

                    for i, line in enumerate(lines, 1):
                        if content_search in line:
                            matching_lines.append({"line": i, "text": line.rstrip()})

                    if matching_lines:
                        matches.append(
                            {
                                "filepath": filepath,
                                "matches": len(matching_lines),
                                "lines": matching_lines,
                            }
                        )
            except:
                # Skip binary files or permissions issues
                continue

        return matches

    def get_project_structure(self, max_depth: int = 3) -> str:
        """Get directory tree structure

        Args:
            max_depth: Maximum directory depth

        Returns:
            Formatted directory tree
        """
        structure = f"📁 Project: {self.base_path.name}\n"

        for root, dirs, files in os.walk(self.base_path):
            # Calculate depth
            depth = root[len(str(self.base_path)) + len(os.sep) :].count(os.sep)

            if depth >= max_depth:
                dirs[:] = []  # Don't go deeper
                continue

            # Don't show hidden directories
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            level = "  " * depth
            folder_name = Path(root).name or self.base_path.name
            structure += f"{level}├── 📁 {folder_name}/\n"

            # Show first 3 files per directory
            file_level = "  " * (depth + 1)
            for i, file in enumerate(files[:3]):
                if not file.startswith("."):
                    structure += f"{file_level}├── {file}\n"

            if len(files) > 3:
                structure += f"{file_level}└── ... ({len(files) - 3} more)\n"

        return structure

    def copy_file(self, src: str, dest: str) -> Dict[str, Union[bool, str]]:
        """Copy file from source to destination

        Args:
            src: Source file path
            dest: Destination path

        Returns:
            Success status
        """
        src_path = self._resolve_path(src)
        dest_path = self._resolve_path(dest)

        if not src_path.exists():
            return {
                "success": False,
                "message": f"❌ Source not found: {src_path}",
                "type": "error",
            }

        if dest_path.exists():
            return {
                "success": False,
                "message": f"❌ Destination exists: {dest_path}",
                "type": "error",
            }

        try:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_text(src_path.read_text(encoding="utf-8"), encoding="utf-8")

            return {
                "success": True,
                "message": f"📄 Copied {src_path} → {dest_path}",
                "type": "copied",
            }
        except Exception as e:
            return {"success": False, "message": f"❌ Error copying: {e}", "type": "error"}

    def _resolve_path(self, filepath: str) -> Path:
        """Resolve relative or absolute path"""
        path = Path(filepath)

        # If absolute, use as is
        if path.is_absolute():
            return path

        # If relative, resolve from base_path
        return self.base_path / path


# Convenience functions
file_manager = FileManager()


def create_file(filepath, content):
    """Create file (for nanobot)"""
    result = file_manager.create_file(filepath, content)
    return result["message"]


def read_file(filepath, preview_lines=None):
    """Read file (for nanobot)"""
    result = file_manager.read_file(filepath, preview_lines)
    return result["message"]


# If preview_lines specified, add content preview
if preview_lines and result.get("content"):
    return f"{result['message']}\n\n{result['content'][:500]}"

return result["message"]


def modify_file(filepath, operations):
    """Modify file (for nanobot)"""
    result = file_manager.modify_file(filepath, operations)
    return result["message"]


def delete_file(filepath, confirm=False):
    """Delete file (for nanobot)"""
    result = file_manager.delete_file(filepath, confirm)
    return result["message"]


def list_files(pattern="*", directory="."):
    """List files (for nanobot)"""
    files = file_manager.list_files(pattern, directory)
    if files:
        return "📁 Files:\n\n" + "\n".join(f"  ✓ {f}" for f in files[:20])
    else:
        return "No files found"


def search_files(pattern, content_search):
    """Search files (for nanobot)"""
    matches = file_manager.search_files(pattern, content_search)
    if matches:
        result = f"🔍 Found {len(matches)} files matching '{content_search}':\n\n"
        for match in matches:
            result += f"✓ {match['filepath']}\n"
            result += f"  Matches: {match['matches']}\n"
            for line in match["lines"][:3]:
                result += f"    Line {line['line']}: {line['text'][:100]}...\n"
            result += "\n"
        return result
    else:
        return f"No files found matching '{content_search}'"


def get_project_structure(max_depth=3):
    """Get project structure (for nanobot)"""
    return file_manager.get_project_structure(max_depth)


def copy_file(src, dest):
    """Copy file (for nanobot)"""
    result = file_manager.copy_file(src, dest)
    return result["message"]
