"""MCP Server entry point for OpenCode Skills management."""

from mcp.types import TextContent
from mcp.server.fastmcp import FastMCP

from .logging_config import setup_logging
from .models import (
    ListSkillsInput,
    GetSkillInfoInput,
    InstallSkillInput,
    UninstallSkillInput,
    SearchSkillsInput,
    ValidateSkillInput,
    GetCombinationsInput,
    InstallWorkflowInput,
)
from .skill_manager import SkillManager

# Setup logging
logger = setup_logging(level="INFO", log_file="logs/opencode_skills_mcp.log")
logger.info("OpenCode Skills MCP Server starting up...")

# Create server instance
server = FastMCP("opencode-skills-mcp")

@server.tool()
async def list_skills(arguments: ListSkillsInput) -> list[TextContent]:
    """List all available OpenCode skills with optional filtering by category or depth. Shows installation status."""
    manager = SkillManager()
    result = manager.list_skills(
        category=arguments.category,
        depth=arguments.depth,
        installed_only=arguments.installed_only
    )
    return [TextContent(type="text", text=result)]

@server.tool()
async def get_skill_info(arguments: GetSkillInfoInput) -> list[TextContent]:
    """Get detailed information about a specific OpenCode skill including description, prerequisites, and installation status."""
    manager = SkillManager()
    result = manager.get_skill_info(arguments.skill_name)
    return [TextContent(type="text", text=result)]

@server.tool()
async def install_skill(arguments: InstallSkillInput) -> list[TextContent]:
    """Install an OpenCode skill globally or locally to your project. Automatically handles file copying."""
    manager = SkillManager()
    result = manager.install_skill(arguments.skill_name, arguments.scope)
    return [TextContent(type="text", text=result)]

@server.tool()
async def uninstall_skill(arguments: UninstallSkillInput) -> list[TextContent]:
    """Uninstall an OpenCode skill from global or local installation directory."""
    manager = SkillManager()
    result = manager.uninstall_skill(arguments.skill_name, arguments.scope)
    return [TextContent(type="text", text=result)]

@server.tool()
async def search_skills(arguments: SearchSkillsInput) -> list[TextContent]:
    """Search for OpenCode skills by keywords, description, or category name."""
    manager = SkillManager()
    result = manager.search_skills(arguments.query)
    return [TextContent(type="text", text=result)]

@server.tool()
async def validate_skill(arguments: ValidateSkillInput) -> list[TextContent]:
    """Validate a skill's SKILL.md file structure for proper YAML frontmatter and required fields."""
    manager = SkillManager()
    result = manager.validate_skill(arguments.skill_path)
    return [TextContent(type="text", text=result)]

@server.tool()
async def get_combinations(arguments: GetCombinationsInput) -> list[TextContent]:
    """Get recommended skill combinations and workflows with installation status for each skill."""
    manager = SkillManager()
    result = manager.get_combinations(arguments.category)
    return [TextContent(type="text", text=result)]

@server.tool()
async def install_workflow(arguments: InstallWorkflowInput) -> list[TextContent]:
    """Install all skills for a recommended workflow combination (e.g., content-pipeline, product-launch)."""
    manager = SkillManager()
    result = manager.install_workflow(arguments.workflow_name, arguments.scope)
    return [TextContent(type="text", text=result)]

def main():
    """Main entry point for the MCP server."""
    logger.info("Starting OpenCode Skills MCP Server...")
    server.run()

if __name__ == "__main__":
    main()