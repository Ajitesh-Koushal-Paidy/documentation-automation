#!/usr/bin/env python3
"""
Configuration loader for documentation automation scripts
Loads configuration from JSON file or environment variables
"""

import os
import json
from pathlib import Path

class Config:
    """Configuration manager for automation scripts"""

    def __init__(self, config_path=None):
        """
        Initialize configuration

        Args:
            config_path: Path to config.json file. If None, looks in standard locations.
        """
        self.config = self._load_config(config_path)

    def _load_config(self, config_path):
        """Load configuration from file"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)

        # Try standard locations
        possible_paths = [
            Path(__file__).parent.parent / "config" / "config.json",
            Path.home() / ".config" / "doc-automation" / "config.json",
            Path("config/config.json"),
        ]

        for path in possible_paths:
            if path.exists():
                with open(path, 'r') as f:
                    return json.load(f)

        # Fallback to empty config (will use environment variables)
        return {}

    def get(self, key, default=None):
        """Get configuration value with fallback to environment variable"""
        # Try nested key (e.g., "paths.baseDir")
        if '.' in key:
            parts = key.split('.')
            value = self.config
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    value = None
                    break
            if value is not None:
                return value
        else:
            if key in self.config:
                return self.config[key]

        # Fallback to environment variable
        env_key = key.upper().replace('.', '_')
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value

        return default

    @property
    def base_dir(self):
        """Get base directory path"""
        return self.get('paths.baseDir', os.path.expanduser('~'))

    @property
    def repo_path(self):
        """Get repository path"""
        return self.get('paths.repoPath', f"{self.base_dir}/repo")

    @property
    def screenshots_dir(self):
        """Get screenshots directory"""
        return self.get('paths.screenshotsDir', f"{self.base_dir}/screenshots")

    @property
    def docs_path(self):
        """Get docs path"""
        return self.get('paths.docsPath', f"{self.base_dir}/docs")

    @property
    def confluence_url(self):
        """Get Confluence URL"""
        return self.get('confluence.url', os.getenv('CONFLUENCE_URL', ''))

    @property
    def confluence_email(self):
        """Get Confluence email"""
        return self.get('confluence.email', os.getenv('CONFLUENCE_EMAIL', ''))

    @property
    def confluence_token(self):
        """Get Confluence API token"""
        return self.get('confluence.token', os.getenv('CONFLUENCE_API_TOKEN', ''))

    @property
    def figma_token(self):
        """Get Figma token"""
        return self.get('figma.token', os.getenv('FIGMA_TOKEN', ''))

    def get_page_id(self, page_name):
        """Get Confluence page ID by name"""
        return self.get(f'pages.{page_name}.id', '')


# Global config instance
_config = None

def get_config(config_path=None):
    """Get global configuration instance"""
    global _config
    if _config is None:
        _config = Config(config_path)
    return _config
