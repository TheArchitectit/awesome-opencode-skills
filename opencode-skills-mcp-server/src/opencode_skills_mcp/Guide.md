# OpenCode MCP Server Setup Troubleshooting Summary

## Introduction
This document summarizes the issues encountered while setting up the OpenCode MCP server from the repository [https://github.com/TheArchitectit/awesome-opencode-skills](https://github.com/TheArchitectit/awesome-opencode-skills). It covers root causes, corrective steps, and the final outcome.

## Issues Faced
- Configuration validation errors in `opencode.json` (e.g., "Invalid input mcp.opencode_skills").
- Module import failures (e.g., "No module named opencode_skills_mcp").
- Import errors in `server.py` (e.g., "Tool not found in mcp.server.models").
- Attribute errors (e.g., "Server has no add_tool method").
- Runtime errors (e.g., "asyncio already running").
- Server loads in OpenCode but remains disabled.

## Root Causes
- **Outdated MCP library API**: The code used old `Server` and `Tool` imports incompatible with MCP 1.26.0.
- **Incorrect package structure**: Missing `src/` layout and `__main__.py`.
- **Config key naming restrictions and command path issues** (e.g., `python3` not in PATH).
- **Asyncio conflicts** from mismatched event loop handling.
- **Python environment differences** between manual runs and OpenCode's execution.

## Steps Taken
- **Fixed Config Key**: Tried various keys (`opencode-skills`, `opencode_skills`, `opencode-skills-mcp`) until `"opencode-skills"` worked.
- **Resolved Python Path**: Switched from `python3` to `python` in the config for Windows compatibility.
- **Updated Package Structure**: Modified `pyproject.toml` for `src/` layout, added `__main__.py`, and reinstalled the package.
- **Fixed Imports**: Updated imports in `server.py` to `from mcp.types import TextContent` and `from mcp.server.fastmcp import FastMCP`.
- **Migrated to FastMCP**: Replaced `Server` with `FastMCP` and used `@server.tool` decorators instead of `add_tool`.
- **Resolved Asyncio Issues**: Made `main()` synchronous and call `main()` directly in the module entry point to avoid event loop conflicts.
- **Enabled Server**: Verified config validity and toggled enable in OpenCode.

## Final Result
The MCP server now loads and enables successfully in OpenCode. All 8 skills (e.g., `list_skills`, `install_skill`) are accessible via AI interactions. The setup is compatible with the current MCP version. Users can fork the repository and submit a pull request with these fixes for upstream integration. No manual server starts are required—OpenCode manages it automatically.

