"""MCP Server entry point for OpenCode Skills management."""

import asyncio
from mcp.server.models import Tool, TextContent
from mcp.server import Server
from mcp.server.stdio import stdio_server

from .config import get_config
from .logging_config import setup_logging, get_logger
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


async def list_skills_handler(arguments: ListSkillsInput) -> list[TextContent]:
    """Handle list_skills tool call."""
    manager = SkillManager()
    result = manager.list_skills(
        category=arguments.category,
        depth=arguments.depth,
        installed_only=arguments.installed_only
    )
    return [TextContent(type="text", text=result)]


async def get_skill_info_handler(arguments: GetSkillInfoInput) -> list[TextContent]:
    """Handle get_skill_info tool call."""
    manager = SkillManager()
    result = manager.get_skill_info(arguments.skill_name)
    return [TextContent(type="text", text=result)]


async def install_skill_handler(arguments: InstallSkillInput) -> list[TextContent]:
    """Handle install_skill tool call."""
    manager = SkillManager()
    result = manager.install_skill(arguments.skill_name, arguments.scope)
    return [TextContent(type="text", text=result)]


async def uninstall_skill_handler(arguments: UninstallSkillInput) -> list[TextContent]:
    """Handle uninstall_skill tool call."""
    manager = SkillManager()
    result = manager.uninstall_skill(arguments.skill_name, arguments.scope)
    return [TextContent(type="text", text=result)]


async def search_skills_handler(arguments: SearchSkillsInput) -> list[TextContent]:
    """Handle search_skills tool call."""
    manager = SkillManager()
    result = manager.search_skills(arguments.query)
    return [TextContent(type="text", text=result)]


async def validate_skill_handler(arguments: ValidateSkillInput) -> list[TextContent]:
    """Handle validate_skill tool call."""
    manager = SkillManager()
    result = manager.validate_skill(arguments.skill_path)
    return [TextContent(type="text", text=result)]


async def get_combinations_handler(arguments: GetCombinationsInput) -> list[TextContent]:
    """Handle get_combinations tool call."""
    manager = SkillManager()
    result = manager.get_combinations(arguments.category)
    return [TextContent(type="text", text=result)]


async def install_workflow_handler(arguments: InstallWorkflowInput) -> list[TextContent]:
    """Handle install_workflow tool call."""
    manager = SkillManager()
    result = manager.install_workflow(arguments.workflow_name, arguments.scope)
    return [TextContent(type="text", text=result)]


def create_server() -> Server:
    """
    Create and configure the MCP server with all tools registered.

    Returns:
        Configured MCP Server instance
    """
    server = Server("opencode-skills-mcp")
    logger.info("Registering tools...")

    # Register tools with proper annotations
    server.add_tool(
        Tool(
            name="list_skills",
            description="List all available OpenCode skills with optional filtering by category or depth. Shows installation status.",
            inputSchema=ListSkillsInput.model_json_schema()
        )
    )

    server.add_tool(
        Tool(
            name="get_skill_info",
            description="Get detailed information about a specific OpenCode skill including description, prerequisites, and installation status.",
            inputSchema=GetSkillInfoInput.model_json_schema()
        )
    )

    server.add_tool(
        Tool(
            name="install_skill",
            description="Install an OpenCode skill globally or locally to your project. Automatically handles file copying.",
            inputSchema=InstallSkillInput.model_json_schema(),
            destructiveHint=False,
            idempotentHint=True
        )
    )

    server.add_tool(
        Tool(
            name="uninstall_skill",
            description="Uninstall an OpenCode skill from global or local installation directory.",
            inputSchema=UninstallSkillInput.model_json_schema(),
            destructiveHint=True
        )
    )

    server.add_tool(
        Tool(
            name="search_skills",
            description="Search for OpenCode skills by keywords, description, or category name.",
            inputSchema=SearchSkillsInput.model_json_schema(),
            readOnlyHint=True
        )
    )

    server.add_tool(
        Tool(
            name="validate_skill",
            description="Validate a skill's SKILL.md file structure for proper YAML frontmatter and required fields.",
            inputSchema=ValidateSkillInput.model_json_schema(),
            readOnlyHint=True
        )
    )

    server.add_tool(
        Tool(
            name="get_combinations",
            description="Get recommended skill combinations and workflows with installation status for each skill.",
            inputSchema=GetCombinationsInput.model_json_schema(),
            readOnlyHint=True
        )
    )

    server.add_tool(
        Tool(
            name="install_workflow",
            description="Install all skills for a recommended workflow combination (e.g., content-pipeline, product-launch).",
            inputSchema=InstallWorkflowInput.model_json_schema(),
            destructiveHint=False,
            idempotentHint=True
        )
    )

    logger.info(f"Registered 8 tools successfully")
    return server


async def main():
    """Main entry point for the MCP server."""
    logger.info("Starting OpenCode Skills MCP Server...")

    server = create_server()

    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server ready, waiting for connections...")
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
