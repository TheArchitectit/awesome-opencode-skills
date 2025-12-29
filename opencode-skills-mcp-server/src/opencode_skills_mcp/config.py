"""Configuration management for OpenCode Skills MCP Server."""

import json
from pathlib import Path
from typing import Any, Optional
from .logging_config import get_logger


logger = get_logger(__name__)


class Config:
    """Configuration management for MCP server."""

    def __init__(self, skills_dir: Optional[Path] = None):
        """
        Initialize configuration.

        Args:
            skills_dir: Path to skills directory (default: parent of this package)
        """
        # Skills directory
        if skills_dir is None:
            self.skills_dir = Path(__file__).parent.parent.parent
        else:
            self.skills_dir = skills_dir

        # Skills metadata file
        self.skills_metadata_file = self.skills_dir / "skills_metadata.json"

        # Character limit for responses
        self.character_limit = 25000

        # OpenCode installation directories
        self.opencode_global = Path.home() / ".config" / "opencode" / "skill"
        self.opencode_project = Path(".opencode") / "skill"

        logger.debug(f"Initialized with skills_dir: {self.skills_dir}")

    def load_skills_metadata(self) -> dict[str, Any]:
        """
        Load skills metadata from JSON file.

        Returns:
            Dictionary of skill metadata
        """
        try:
            if self.skills_metadata_file.exists():
                with open(self.skills_metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    logger.debug(f"Loaded metadata for {len(metadata)} skills")
                    return metadata
            else:
                logger.warning(f"Skills metadata file not found: {self.skills_metadata_file}")
                return {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse skills metadata JSON: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error loading skills metadata: {e}")
            return {}

    def get_install_dir(self, scope: str = "global") -> Path:
        """
        Get installation directory based on scope.

        Args:
            scope: 'global' or 'project'

        Returns:
            Path to installation directory
        """
        if scope == "project":
            return self.opencode_project
        elif scope == "global":
            return self.opencode_global
        else:
            logger.warning(f"Invalid scope '{scope}', using 'global'")
            return self.opencode_global

    def is_skill_installed(self, skill_name: str, scope: str = "global") -> bool:
        """
        Check if a skill is installed.

        Args:
            skill_name: Name of the skill
            scope: 'global' or 'project'

        Returns:
            True if installed, False otherwise
        """
        install_dir = self.get_install_dir(scope)
        skill_path = install_dir / skill_name

        if not skill_path.exists():
            return False

        skill_md = skill_path / "SKILL.md"
        is_installed = skill_md.exists()

        logger.debug(f"Skill '{skill_name}' installed: {is_installed} (scope: {scope})")
        return is_installed


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get global configuration instance.

    Returns:
        Config instance
    """
    global _config
    if _config is None:
        _config = Config()
    return _config
