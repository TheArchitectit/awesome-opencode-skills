"""Skill management logic for OpenCode Skills MCP Server."""

import re
import shutil
from pathlib import Path
from typing import Any

from .config import Config, get_config
from .logging_config import get_logger


logger = get_logger(__name__)


class SkillManager:
    """Manages OpenCode skills operations."""

    def __init__(self):
        """Initialize skill manager with configuration."""
        self.config = get_config()
        self.combinations = {
            "content-pipeline": {
                "name": "Content Creation Pipeline",
                "description": "Create professional blog posts with images and branding",
                "skills": ["content-research-writer", "image-enhancer", "canvas-design", "brand-guidelines"],
                "category": "Writing"
            },
            "product-launch": {
                "name": "Product Launch Workflow",
                "description": "Complete product launch preparation from domain to documentation",
                "skills": [
                    "domain-name-brainstormer", "competitive-ads-extractor",
                    "lead-research-assistant", "content-research-writer",
                    "artifacts-builder", "theme-factory", "changelog-generator"
                ],
                "category": "Business"
            },
            "development-cycle": {
                "name": "Developer Productivity Cycle",
                "description": "Daily development workflow - testing, documentation, organization",
                "skills": ["webapp-testing", "changelog-generator", "skill-creator", "file-organizer"],
                "category": "Development"
            },
            "document-workflow": {
                "name": "Professional Document Workflow",
                "description": "Create professional business documents with proper formatting",
                "skills": ["docx", "pdf", "image-enhancer", "brand-guidelines", "internal-comms"],
                "category": "Document Processing"
            },
            "visual-campaign": {
                "name": "Visual Marketing Campaign",
                "description": "Create marketing assets with consistent branding",
                "skills": [
                    "canvas-design", "theme-factory", "image-enhancer",
                    "brand-guidelines", "slack-gif-creator"
                ],
                "category": "Visual"
            }
        }

    def list_skills(
        self,
        category: str | None = None,
        depth: str | None = None,
        installed_only: bool = False
    ) -> str:
        """
        List available skills with optional filtering.

        Args:
            category: Filter by category
            depth: Filter by depth
            installed_only: Only show installed skills

        Returns:
            Formatted markdown string of skills
        """
        metadata = self.config.load_skills_metadata()

        logger.debug(f"Filtering skills: category={category}, depth={depth}, installed_only={installed_only}")

        # Apply filters
        if category:
            metadata = {k: v for k, v in metadata.items() if v.get("category") == category}
            logger.debug(f"Filtered to {len(metadata)} skills by category '{category}'")

        if depth:
            metadata = {k: v for k, v in metadata.items() if v.get("depth") == depth}
            logger.debug(f"Filtered to {len(metadata)} skills by depth '{depth}'")

        if installed_only:
            metadata = {k: v for k, v in metadata.items() if self.config.is_skill_installed(k)}
            logger.debug(f"Filtered to {len(metadata)} installed skills")

        if not metadata:
            logger.warning("No skills found matching criteria")
            return "# Skills\n\nNo skills found matching your criteria."

        result = "# Available OpenCode Skills\n\n"

        for skill_name, skill_data in metadata.items():
            installed_mark = " ✅" if self.config.is_skill_installed(skill_name) else ""
            depth_icon = "📖" if skill_data.get("depth") == "Comprehensive" else "📄"

            result += f"## {depth_icon} {skill_name}{installed_mark}\n\n"
            result += f"**Description**: {skill_data.get('description', 'N/A')}\n\n"
            result += f"**Category**: {skill_data.get('category', 'N/A')}\n\n"
            result += f"**Depth**: {skill_data.get('depth', 'N/A')}\n\n"
            result += f"**Lines**: {skill_data.get('lines', 'N/A')}\n\n"
            result += f"**Prerequisites**: {skill_data.get('prerequisites', 'None')}\n\n"
            result += "---\n\n"

        # Truncate if too long
        if len(result) > self.config.character_limit:
            logger.warning(f"Output truncated from {len(result)} to {self.config.character_limit}")
            result = result[:self.config.character_limit] + "\n\n[Output truncated due to length limit]"

        return result

    def get_skill_info(self, skill_name: str) -> str:
        """
        Get detailed information about a specific skill.

        Args:
            skill_name: Name of the skill

        Returns:
            Formatted markdown string with skill details
        """
        metadata = self.config.load_skills_metadata()

        if skill_name not in metadata:
            logger.warning(f"Skill '{skill_name}' not found")
            return f"# Error\n\nSkill '{skill_name}' not found. Use list_skills to see available skills."

        skill_data = metadata[skill_name]
        installed_status = "✅ Installed" if self.config.is_skill_installed(skill_name) else "⬜ Not installed"

        result = f"# {skill_name}\n\n"
        result += f"**Status**: {installed_status}\n\n"
        result += f"**Description**: {skill_data.get('description', 'N/A')}\n\n"
        result += f"**Category**: {skill_data.get('category', 'N/A')}\n\n"
        result += f"**Depth**: {skill_data.get('depth', 'N/A')}\n\n"
        result += f"**Documentation Lines**: {skill_data.get('lines', 'N/A')}\n\n"
        result += f"**Prerequisites**:\n```\n{skill_data.get('prerequisites', 'None')}\n```\n\n"
        result += f"**Keywords**: {', '.join(skill_data.get('keywords', []))}\n\n"

        if self.config.is_skill_installed(skill_name):
            result += f"**Location**: {self.config.opencode_global / skill_name}\n\n"

        logger.debug(f"Returning info for skill '{skill_name}'")
        return result

    def install_skill(self, skill_name: str, scope: str = "global") -> str:
        """
        Install an OpenCode skill.

        Args:
            skill_name: Name of the skill to install
            scope: 'global' or 'project'

        Returns:
            Formatted result string
        """
        metadata = self.config.load_skills_metadata()

        if skill_name not in metadata:
            logger.error(f"Skill '{skill_name}' not found in metadata")
            return f"# Error\n\nSkill '{skill_name}' not found. Use list_skills to see available skills."

        install_dir = self.config.get_install_dir(scope)
        install_dir.mkdir(parents=True, exist_ok=True)

        skill_path = self.config.skills_dir / skill_name

        if not skill_path.exists():
            logger.error(f"Skill directory not found: {skill_path}")
            return f"# Error\n\nSkill directory '{skill_name}' not found in skills directory."

        dest_path = install_dir / skill_name

        if dest_path.exists():
            logger.warning(f"Skill '{skill_name}' already installed at {dest_path}")
            return f"# Installation Skipped\n\nSkill '{skill_name}' is already installed at {dest_path}"

        try:
            shutil.copytree(skill_path, dest_path)
            logger.info(f"Successfully installed '{skill_name}' to {dest_path}")

            result = f"✅ Successfully installed '{skill_name}'\n\n"
            result += f"**Location**: {dest_path}\n"
            result += f"**Scope**: {scope}\n\n"
            result += f"**Prerequisites**: {metadata[skill_name].get('prerequisites', 'None')}\n\n"
            result += "Note: Restart OpenCode to load the new skill."
            return result
        except Exception as e:
            logger.error(f"Failed to install '{skill_name}': {e}")
            return f"# Error\n\n❌ Failed to install '{skill_name}': {str(e)}"

    def uninstall_skill(self, skill_name: str, scope: str = "global") -> str:
        """
        Uninstall an OpenCode skill.

        Args:
            skill_name: Name of the skill to uninstall
            scope: 'global' or 'project'

        Returns:
            Formatted result string
        """
        install_dir = self.config.get_install_dir(scope)
        skill_path = install_dir / skill_name

        if not skill_path.exists():
            logger.warning(f"Skill '{skill_name}' not installed")
            return f"# Error\n\nSkill '{skill_name}' is not installed."

        try:
            shutil.rmtree(skill_path)
            logger.info(f"Successfully uninstalled '{skill_name}' from {skill_path}")

            result = f"✅ Successfully uninstalled '{skill_name}'\n\n"
            result += f"**Location removed**: {skill_path}\n"
            result += "Note: Restart OpenCode to update the skill list."
            return result
        except Exception as e:
            logger.error(f"Failed to uninstall '{skill_name}': {e}")
            return f"# Error\n\n❌ Failed to uninstall '{skill_name}': {str(e)}"

    def search_skills(self, query: str) -> str:
        """
        Search for skills by keywords or description.

        Args:
            query: Search query string

        Returns:
            Formatted markdown string of matches
        """
        metadata = self.config.load_skills_metadata()
        query_lower = query.lower()

        logger.debug(f"Searching for skills with query: {query}")

        matches = []
        for skill_name, skill_data in metadata.items():
            description = skill_data.get('description', '').lower()
            keywords = [k.lower() for k in skill_data.get('keywords', [])]
            category = skill_data.get('category', '').lower()

            if (query_lower in description or
                any(query_lower in k for k in keywords) or
                query_lower in category or
                query_lower in skill_name.lower()):
                matches.append((skill_name, skill_data))

        logger.debug(f"Found {len(matches)} matching skills")

        if not matches:
            return f"# Search Results\n\nNo skills found matching '{query}'. Try different keywords."

        result = f"# Search Results for '{query}'\n\n"

        for skill_name, skill_data in matches:
            installed_mark = " ✅" if self.config.is_skill_installed(skill_name) else ""
            result += f"## {skill_name}{installed_mark}\n\n"
            result += f"**Category**: {skill_data.get('category', 'N/A')}\n\n"
            result += f"**Description**: {skill_data.get('description', 'N/A')}\n\n"
            result += "---\n\n"

        if len(result) > self.config.character_limit:
            logger.warning(f"Search output truncated from {len(result)} to {self.config.character_limit}")
            result = result[:self.config.character_limit] + "\n\n[Output truncated due to length limit]"

        return result

    def validate_skill(self, skill_path_str: str) -> str:
        """
        Validate a skill's SKILL.md file structure.

        Args:
            skill_path_str: Path string to skill directory

        Returns:
            Formatted validation result string
        """
        skill_path = Path(skill_path_str)
        skill_md = skill_path / "SKILL.md"

        if not skill_md.exists():
            logger.error(f"SKILL.md not found at {skill_md}")
            return f"# Validation Error\n\nSKILL.md not found at {skill_md}"

        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Failed to read SKILL.md: {e}")
            return f"# Validation Error\n\nFailed to read SKILL.md: {str(e)}"

        # Check for YAML frontmatter
        if not content.startswith('---'):
            return "# Validation Error\n\n❌ Invalid: Missing YAML frontmatter (must start with '---')"

        # Check for required fields
        frontmatter_end = content.find('---', 3)
        if frontmatter_end == -1:
            return "# Validation Error\n\n❌ Invalid: Missing closing '---' in YAML frontmatter"

        frontmatter = content[:frontmatter_end]
        required_fields = ['name', 'description']
        missing_fields = [field for field in required_fields if field not in frontmatter]

        if missing_fields:
            return f"# Validation Error\n\n❌ Invalid: Missing required YAML fields: {', '.join(missing_fields)}"

        # Check skill name format
        name_match = re.search(r'name:\s*(.+)', frontmatter)
        if name_match:
            skill_name = name_match.group(1).strip()
            if ' ' in skill_name or not re.match(r'^[a-z0-9-]+$', skill_name):
                error_msg = f"❌ Invalid: Skill name '{skill_name}' should be hyphen-case (no spaces, lowercase letters, numbers, hyphens)"
                logger.error(f"Invalid skill name format: {skill_name}")
                return f"# Validation Error\n\n{error_msg}"

        logger.info(f"Skill at {skill_path} is valid")
        return "# Validation Result\n\n✅ Valid: Skill SKILL.md structure is correct"

    def get_combinations(self, category: str | None = None) -> str:
        """
        Get recommended skill combinations.

        Args:
            category: Filter by workflow category

        Returns:
            Formatted markdown string of combinations
        """
        combinations = self.combinations.copy()

        if category:
            combinations = {k: v for k, v in combinations.items() if v.get("category") == category}
            logger.debug(f"Filtered combinations to category: {category}")

        if not combinations:
            logger.warning("No combinations found")
            return "# Skill Combinations\n\nNo combinations found matching your criteria."

        result = "# Recommended Skill Combinations\n\n"

        for combo_key, combo_data in combinations.items():
            result += f"## {combo_data['name']}\n\n"
            result += f"**Description**: {combo_data['description']}\n\n"
            result += f"**Category**: {combo_data.get('category', 'N/A')}\n\n"
            result += f"**Skills**: {', '.join(combo_data['skills'])}\n\n"

            # Check which skills are installed
            installed = [s for s in combo_data['skills'] if self.config.is_skill_installed(s)]
            missing = [s for s in combo_data['skills'] if not self.config.is_skill_installed(s)]

            if installed:
                result += f"**Already installed**: {', '.join(installed)}\n\n"
            if missing:
                result += f"**Need to install**: {', '.join(missing)}\n\n"

            result += f"**Install workflow**: `install_workflow --workflow-name {combo_key}`\n\n"
            result += "---\n\n"

        if len(result) > self.config.character_limit:
            logger.warning(f"Combinations output truncated from {len(result)} to {self.config.character_limit}")
            result = result[:self.config.character_limit] + "\n\n[Output truncated due to length limit]"

        return result

    def install_workflow(self, workflow_name: str, scope: str = "global") -> str:
        """
        Install all skills for a recommended workflow.

        Args:
            workflow_name: Name of the workflow
            scope: 'global' or 'project'

        Returns:
            Formatted result string
        """
        if workflow_name not in self.combinations:
            logger.error(f"Workflow '{workflow_name}' not found")
            return f"# Error\n\nWorkflow '{workflow_name}' not found. Use get_combinations to see available workflows."

        skills_to_install = self.combinations[workflow_name]['skills']
        install_dir = self.config.get_install_dir(scope)
        install_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Installing workflow '{workflow_name}' with {len(skills_to_install)} skills")

        result = f"# Installing '{workflow_name}' Workflow\n\n"
        result += f"**Scope**: {scope}\n\n"
        result += "**Skills to install**:\n\n"

        installed_count = 0
        failed_count = 0

        for skill_name in skills_to_install:
            skill_path = self.config.skills_dir / skill_name
            dest_path = install_dir / skill_name

            result += f"- {skill_name}: "

            if dest_path.exists():
                result += "⚠️ Already installed\n"
                installed_count += 1
                logger.debug(f"Skill '{skill_name}' already installed")
            elif skill_path.exists():
                try:
                    shutil.copytree(skill_path, dest_path)
                    result += "✅ Installed\n"
                    installed_count += 1
                    logger.info(f"Installed '{skill_name}' to {dest_path}")
                except Exception as e:
                    result += f"❌ Failed: {str(e)}\n"
                    failed_count += 1
                    logger.error(f"Failed to install '{skill_name}': {e}")
            else:
                result += "❌ Not found in skills directory\n"
                failed_count += 1
                logger.warning(f"Skill directory '{skill_path}' not found")

        result += f"\n**Summary**: {installed_count} installed, {failed_count} failed\n\n"
        result += "Note: Restart OpenCode to load new skills."

        return result
