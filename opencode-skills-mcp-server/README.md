# OpenCode Skills MCP Server

A Model Context Protocol (MCP) server that makes managing OpenCode skills easier.

## Features

- **List Skills**: Browse all available skills with filtering by category, depth, or installation status
- **Get Skill Info**: View detailed information about any skill including prerequisites
- **Install/Uninstall**: Easily install or remove skills from global or local directories
- **Search Skills**: Find skills by keywords, description, or category
- **Validate Skills**: Check if a skill's SKILL.md has proper structure
- **Get Combinations**: Discover recommended skill combinations for common workflows
- **Install Workflows**: One-command installation of entire skill workflows

## Installation

### Prerequisites

- Python 3.9 or higher
- MCP server libraries (`mcp>=0.1.0`)
- Pydantic for input validation

### Setup

1. **Install Dependencies**:
   ```bash
   cd opencode-skills-mcp-server
   pip install -e .
   # Or using uv:
   uv pip install -e .
   ```

2. **Configure with OpenCode**:

   Add to your OpenCode config (usually `~/.config/opencode/config.json`):

   ```json
   {
     "mcpServers": {
       "opencode-skills": {
         "command": "python",
         "args": ["/path/to/opencode-skills-mcp-server/src/opencode_skills_mcp/server.py"],
         "env": {}
       }
     }
   }
   ```

3. **Restart OpenCode** to load the server.

## Usage

Once configured, you can use the MCP server tools from OpenCode:

### List All Skills

```
/list_skills
```

Filter by category:
```
/list_skills --category "Development"
```

Filter by depth:
```
/list_skills --depth "Comprehensive"
```

Show only installed:
```
/list_skills --installed-only
```

### Get Skill Information

```
/get_skill_info --skill-name "content-research-writer"
```

### Install a Skill

Globally:
```
/install_skill --skill-name "file-organizer" --scope "global"
```

Locally (for current project):
```
/install_skill --skill-name "changelog-generator" --scope "project"
```

### Uninstall a Skill

```
/uninstall_skill --skill-name "old-skill" --scope "global"
```

### Search for Skills

```
/search_skills --query "document"
```

```
/search_skills --query "testing automation"
```

### Validate a Skill

```
/validate_skill --skill-path "/path/to/skill"
```

### Get Skill Combinations

```
/get_combinations
```

Filter by category:
```
/get_combinations --category "Writing"
```

### Install a Workflow

```
/install_workflow --workflow-name "content-pipeline" --scope "global"
```

Available workflows:
- `content-pipeline` - Content Creation Pipeline
- `product-launch` - Product Launch Workflow
- `development-cycle` - Developer Productivity Cycle
- `document-workflow` - Professional Document Workflow
- `visual-campaign` - Visual Marketing Campaign

## Logging

Logs are written to `logs/opencode_skills_mcp.log` for debugging.

To enable debug logging, modify `server.py`:
```python
logger = setup_logging(level="DEBUG", log_file="logs/opencode_skills_mcp.log")
```

## Modularity

The server is structured into separate modules:

- `config.py` - Configuration management
- `logging_config.py` - Logging setup
- `models.py` - Pydantic input/output models
- `skill_manager.py` - Core skill management logic
- `server.py` - MCP server setup and tool registration

## Character Limit

Responses are limited to 25,000 characters to stay within MCP context limits.

## Troubleshooting

### Tools Not Appearing

1. Check OpenCode config has the server registered
2. Verify Python executable path is correct
3. Check logs for errors

### Skill Installation Fails

1. Verify the skill directory exists in the skills folder
2. Check permissions on installation directory
3. Review logs for specific error messages

### Skills Not Found

1. Ensure the MCP server path points to the skills repository root
2. Check that `skills_metadata.json` exists
3. Verify skill names use hyphen-case

## License

MIT
