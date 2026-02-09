"""Configuration module for NotebookLM Backup application."""

import json
from pathlib import Path
from typing import Any

# Default config file path
CONFIG_FILE = Path(__file__).parent / "config.json"


def load_config(config_path: Path | None = None) -> dict[str, Any]:
    """Load configuration from JSON file.
    
    Args:
        config_path: Optional path to config file. Defaults to config.json in project root.
    
    Returns:
        Dictionary containing configuration settings.
    """
    if config_path is None:
        config_path = CONFIG_FILE
    
    if not config_path.exists():
        return get_default_config()
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # Ensure all required keys exist with defaults
    return get_default_config() | config


def get_default_config() -> dict[str, Any]:
    """Get default configuration values."""
    return {
        "output_directory": "./backups",
        "backup_artifact_types": {
            "reports": True,
            "data_tables": True,
            "audio": True,
            "video": True,
            "slides": True,
            "infographics": True,
        },
        "export_artifact_types": {
            "reports": "docs",
            "data_tables": "sheets",
            "slides": "slides",
        },
    }


def get_output_directory(config: dict[str, Any]) -> Path:
    """Get the output directory from config.
    
    Args:
        config: Configuration dictionary.
    
    Returns:
        Path object for the output directory.
    """
    return Path(config["output_directory"])


def get_artifact_types(config: dict[str, Any]) -> dict[str, bool]:
    """Get which artifact types to backup.
    
    Args:
        config: Configuration dictionary.
    
    Returns:
        Dictionary mapping artifact type names to boolean flags.
    """
    return config.get("backup_artifact_types", {})


def get_export_types(config: dict[str, Any]) -> dict[str, str]:
    """Get export target types for artifacts.
    
    Args:
        config: Configuration dictionary.
    
    Returns:
        Dictionary mapping artifact type to export target ("docs", "sheets", "slides").
    """
    return config.get("export_artifact_types", {})
