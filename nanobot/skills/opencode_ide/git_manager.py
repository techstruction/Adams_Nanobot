#!/usr/bin/env python3
"""
OpenCode IDE - Git Manager
Handles git operations for nanobot workspace
"""

import subprocess
import re
from pathlib import Path
from typing import List, Dict, Optional, Union


class GitManager:
    """Manages git operations"""

    def __init__(self, repo_path: str = None):
        """Initialize GitManager

        Args:
            repo_path: Path to git repository
                      (default: /Users/adam/Documents/Nanobot)
        """
        if repo_path:
            self.repo_path = Path(repo_path)
        else:
            self.repo_path = Path.home() / "Documents" / "Nanobot"

    def git_status(self) -> Dict[str, Union[str, bool, List[str]]]:
        """Get git status

        Returns:
            Dict with branch, status, staged, unstaged, untracked
        """
        try:
            # Get current branch
            branch_result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            branch = branch_result.stdout.strip()

            # Get status
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )

            staged = []
            unstaged = []
            untracked = []

            for line in status_result.stdout.strip().split("\n"):
                if not line:
                    continue

                status = line[:2]
                filename = line[3:]

                if status[0] in "AMDR":
                    staged.append(filename)
                elif status[0] == " " and status[1] in "M":
                    unstaged.append(filename)
                elif status == "??":
                    untracked.append(filename)

            return {
                "success": True,
                "branch": branch,
                "staged": staged,
                "unstaged": unstaged,
                "untracked": untracked,
                "clean": not staged and not unstaged and not untracked,
            }
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": f"Git error: {e.stderr}"}

    def git_add(self, files: Union[str, List[str]]) -> str:
        """Stage files for commit

        Args:
            files: Single file, list of files, or directory

        Returns:
            Status message
        """
        if isinstance(files, str):
            files = [files]

        file_paths = []
        for file in files:
            if Path(file).is_dir():
                # For directories, stage all files in it
                file_paths.extend([str(p) for p in Path(file).glob("*")])
            else:
                file_paths.append(file)

        try:
            result = subprocess.run(
                ["git", "add"] + file_paths,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )

            if file_paths:
                return f"✅ Staged {len(file_paths)} files: {', '.join(file_paths[:3])}"
            else:
                return "✅ No files to stage"
        except subprocess.CalledProcessError as e:
            return f"❌ Git error: {e.stderr}"

    def git_commit(self, message: str, files: List[str] = None) -> str:
        """Create commit

        Args:
            message: Commit message
            files: Optional list of specific files (if None, commits staged changes)

        Returns:
            Status message
        """
        try:
            # If specific files provided, stage them first
            if files:
                self.git_add(files)

            # Create commit
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )

            # Extract hash from output
            lines = result.stdout.strip().split("\n")
            for line in lines:
                if line.startswith("[", 0, 15):
                    return f"✅ {line}"  # Contains commit hash

            return "✅ Commit created successfully"
        except subprocess.CalledProcessError as e:
            return f"❌ Git error: {e.stderr}"

    def git_push(self, remote: str = "origin", branch: str = None) -> str:
        """Push to remote repository

        Args:
            remote: Remote name (default: origin)
            branch: Branch name (default: current branch)
        """
        if not branch:
            # Get current branch
            status = self.git_status()
            if not status.get("success"):
                return f"❌ Git error: {status.get('error')}"
            branch = status["branch"]

        try:
            result = subprocess.run(
                ["git", "push", remote, branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )

            return f"✅ Pushed {remote}/{branch}"
        except subprocess.CalledProcessError as e:
            if "has no upstream branch" in e.stderr:
                # First push, set upstream
                return self.git_push_set_upstream(remote, branch)
            return f"❌ Push error: {e.stderr}"

    def git_push_set_upstream(self, remote: str = "origin", branch: str = None) -> str:
        """Push with upstream tracking\n
        Uses: git push --set-upstream origin branch
        """
        if not branch:
            status = self.git_status()
            branch = status["branch"]

        try:
            result = subprocess.run(
                ["git", "push", "--set-upstream", remote, branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )

            return f"✅ Pushed and set upstream {remote}/{branch}"
        except subprocess.CalledProcessError as e:
            return f"❌ Push error: {e.stderr}"

    def git_pull(self, remote: str = "origin", branch: str = None) -> str:
        """Pull from remote repository

        Args:
            remote: Remote name (default: origin)
            branch: Branch name (default: current branch)
        """
        if not branch:
            status = self.git_status()
            branch = status["branch"]

        try:
            result = subprocess.run(
                ["git", "pull", remote, branch], cwd=self.repo_path, capture_output=True, text=True
            )

            if result.returncode == 0:
                output = result.stdout.strip()
                if "Already up to date" in output or "Already up-to-date" in output:
                    return "ℹ️ Already up to date"
                else:
                    # Count changed files
                    changed = []
                    for line in output.split("\n"):
                        if line.startswith(" "):
                            changed.append(line.strip())

                    return f"✅ Pulled {len(changed)} changes from {remote}/{branch}"
            else:
                return f"❌ Pull error: {result.stderr}"
        except Exception as e:
            return f"❌ Pull error: {e}"

    def git_branch(self, name: str, switch: bool = True) -> str:
        """Create and optionally switch to new branch\n
        Args:
            name: New branch name
            switch: Whether to switch to new branch
        """
        try:
            if switch:
                # Create and switch
                result = subprocess.run(
                    ["git", "checkout", "-b", name],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                return f"✅ Created and switched to branch '{name}'"
            else:
                # Just create
                result = subprocess.run(
                    ["git", "branch", name],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                return f"✅ Created branch '{name}'"
        except subprocess.CalledProcessError as e:
            return f"❌ Branch error: {e.stderr}"

    def git_log(self, limit: int = 5, oneline: bool = True) -> str:
        """Get recent commit history\n
        Args:
            limit: Number of commits to show
            oneline: Show in oneline format
        """
        try:
            cmd = ["git", "log"]
            if oneline:
                cmd.extend(["--oneline", f"-{limit}"])
            else:
                cmd.extend(["-n", str(limit)])

            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True, check=True
            )

            return f"📜 Recent commits:\n\n{result.stdout}"
        except subprocess.CalledProcessError as e:
            return f"❌ Log error: {e.stderr}"

    def git_restore(self, filepath: str) -> str:
        """Restore file to last committed state\n
        Args:
            filepath: File to restore
        """
        try:
            result = subprocess.run(
                ["git", "restore", filepath], cwd=self.repo_path, capture_output=True, text=True
            )

            if result.returncode == 0:
                return f"✅ Restored {filepath} to last committed state"
            else:
                return f"❌ Restore error: {result.stderr}"
        except Exception as e:
            return f"❌ Restore error: {e}"

    def git_diff(self, filepath: str = None) -> str:
        """Show git diff for file or entire repository\n
        Args:
            filepath: Optional specific file
        """
        try:
            cmd = ["git", "diff"]
            if filepath:
                cmd.append(filepath)

            result = subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True)

            if result.stdout.strip():
                # Limit output for large diffs
                lines = result.stdout.split("\n")
                if len(lines) > 100:
                    output = "\n".join(lines[:100])
                    output += f"\n\n... (diff truncated, {len(lines) - 100} more lines)"
                else:
                    output = result.stdout

                return f"👁️  Diff:\n\n{output}"
            else:
                return "ℹ️ No differences detected"
        except Exception as e:
            return f"❌ Diff error: {e}"


# Convenience functions for nanobot
git_manager = GitManager()


def git_status():
    """Get git status (for nanobot)"""
    result = git_manager.git_status()

    if not result.get("success"):
        return f"❌ Error: {result.get('error')}"

    output = f"🌿 On branch {result['branch']}\n"

    if result["clean"]:
        output += "✅ Working tree clean\n"
    else:
        if result["staged"]:
            output += "📤 Staged:\n"
            for f in result["staged"]:
                output += f"  + {f}\n"

        if result["unstaged"]:
            output += "📝 Modified:\n"
            for f in result["unstaged"]:
                output += f"  ~ {f}\n"

        if result["untracked"]:
            output += "❓ Untracked:\n"
            for f in result["untracked"]:
                output += f"  ? {f}\n"

    return output


def git_add(files):
    """Stage files (for nanobot)"""
    return git_manager.git_add(files)


def git_commit(message):
    """Commit changes (for nanobot)"""
    return git_manager.git_commit(message)


def git_push(remote="origin", branch=None):
    """Push changes (for nanobot)"""
    return git_manager.git_push(remote, branch)


def git_pull(remote="origin", branch=None):
    """Pull changes (for nanobot)"""
    return git_manager.git_pull(remote, branch)


def git_branch(name, switch=True):
    """Create branch (for nanobot)"""
    return git_manager.git_branch(name, switch)


def git_log(limit=5):
    """Show commit log (for nanobot)"""
    return git_manager.git_log(limit)


def git_diff(filepath=None):
    """Show diff (for nanobot)"""
    return git_manager.git_diff(filepath)
