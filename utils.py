"""Utility functions for NotebookLM Backup application."""

import re
from pathlib import Path
from typing import Any


def sanitize_filename(title: str) -> str:
    """Sanitize a title for use as a filename or folder name.
    
    Args:
        title: The original title string.
    
    Returns:
        A filesystem-safe string with invalid characters replaced by underscores.
    """
    if not title:
        return "untitled"
    
    # Characters that are invalid in file/directory names on most systems
    # : \ / * ? " < > | and control characters
    invalid_chars = r'[\\/*?:"<>|\x00-\x1f]'
    
    # Replace invalid characters with underscores
    sanitized = re.sub(invalid_chars, "_", title)
    
    # Remove leading/trailing spaces and periods
    sanitized = sanitized.strip(" .")
    
    # If result is empty or only underscores, use a default
    if not sanitized or sanitized == "_" * len(sanitized):
        return "untitled"
    
    # Limit length to avoid filesystem issues (255 is safe)
    if len(sanitized) > 250:
        sanitized = sanitized[:250].rstrip("_")
    
    return sanitized


def extract_notebook_id(url: str) -> str | None:
    """Extract notebook ID from a NotebookLM URL.
    
    Args:
        url: The NotebookLM URL (e.g., https://notebooklm.google.com/notebook/abc123)
    
    Returns:
        The notebook ID if found, None otherwise.
    """
    if not url:
        return None
    
    # Match pattern: https://notebooklm.google.com/notebook/{notebook_id}
    pattern = r"notebooklm\.google\.com/notebook/([a-zA-Z0-9_-]+)"
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    
    # If the URL doesn't match, assume it's already a notebook ID
    return url if url else None


def ensure_directory(path: Path) -> Path:
    """Create directory if it doesn't exist.
    
    Args:
        path: The directory path to create.
    
    Returns:
        The Path object for the created directory.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def print_progress(message: str) -> None:
    """Print a progress message.
    
    Args:
        message: The message to print.
    """
    print(f"[PROGRESS] {message}")


def print_summary(message: str) -> None:
    """Print a summary message.
    
    Args:
        message: The message to print.
    """
    print(f"[SUMMARY] {message}")


def print_error(message: str) -> None:
    """Print an error message.
    
    Args:
        message: The error message to print.
    """
    print(f"[ERROR] {message}")
