/**
 * MCP Server - Main entry point
 */

import { Server } from '@modelcontextprotocol/sdk';
import { 
  StdioServerTransport 
} from '@modelcontextprotocol/sdk/stdio';
import { z } from 'zod';

import {
  listSkillsHandler,
  getSkillInfoHandler,
  installSkillHandler,
  uninstallSkillHandler,
  searchSkillsHandler,
  validateSkillHandler,
  getCombinationsHandler,
  installWorkflowHandler
} from './skill-manager.js';

// Character limit for responses
const CHARACTER_LIMIT = 25000;

/**
 * Create and configure MCP server with all tools registered
 */
export function createServer(): Server {
  console.log('[Server] Creating OpenCode Skills MCP Server...');

  const server = new Server(
    {
      name: 'opencode-skills-mcp',
      version: '1.0.0',
    },
    {
      capabilities: {},
    }
  );

  console.log('[Server] Registering tools...');

  // Register tools with proper schemas
  server.addTool({
    name: 'list_skills',
    description: 'List all available OpenCode skills with optional filtering by category or depth. Shows installation status.',
    inputSchema: z.object({
      category: z.string().optional().describe('Filter by skill category (e.g., \'Development\', \'Writing\', \'Document Processing\')'),
      depth: z.string().optional().describe('Filter by depth (e.g., \'Comprehensive\', \'Standard\', \'Quick Reference\')'),
      installed_only: z.boolean().optional().default(false).describe('Only show installed skills'),
    }).strict(),
  });

  server.addTool({
    name: 'get_skill_info',
    description: 'Get detailed information about a specific OpenCode skill including description, prerequisites, and installation status.',
    inputSchema: z.object({
      skill_name: z.string().describe('Name of the skill to get information about'),
    }).strict(),
  });

  server.addTool({
    name: 'install_skill',
    description: 'Install an OpenCode skill globally or locally to your project. Automatically handles file copying.',
    inputSchema: z.object({
      skill_name: z.string().describe('Name of the skill to install'),
      scope: z.enum(['global', 'project']).default('global').describe('Installation scope: \'global\' or \'project\''),
    }).strict(),
  }, {
    destructiveHint: false,
    idempotentHint: true,
  });

  server.addTool({
    name: 'uninstall_skill',
    description: 'Uninstall an OpenCode skill from global or local installation directory.',
    inputSchema: z.object({
      skill_name: z.string().describe('Name of the skill to uninstall'),
      scope: z.enum(['global', 'project']).default('global').describe('Uninstallation scope: \'global\' or \'project\''),
    }).strict(),
  }, {
    destructiveHint: true,
  });

  server.addTool({
    name: 'search_skills',
    description: 'Search for OpenCode skills by keywords, description, or category name.',
    inputSchema: z.object({
      query: z.string().describe('Search query (keywords or description)'),
    }).strict(),
  }, {
    readOnlyHint: true,
  });

  server.addTool({
    name: 'validate_skill',
    description: 'Validate a skill\'s SKILL.md file structure for proper YAML frontmatter and required fields.',
    inputSchema: z.object({
      skill_path: z.string().describe('Path to the skill directory to validate'),
    }).strict(),
  }, {
    readOnlyHint: true,
  });

  server.addTool({
    name: 'get_combinations',
    description: 'Get recommended skill combinations and workflows with installation status for each skill.',
    inputSchema: z.object({
      category: z.string().optional().describe('Filter by workflow category (e.g., \'Writing\', \'Development\', \'Business\')'),
    }).strict(),
  }, {
    readOnlyHint: true,
  });

  server.addTool({
    name: 'install_workflow',
    description: 'Install all skills for a recommended workflow combination (e.g., content-pipeline, product-launch).',
    inputSchema: z.object({
      workflow_name: z.string().describe('Name of the workflow to install (e.g., \'content-pipeline\', \'product-launch\', \'development-cycle\')'),
      scope: z.enum(['global', 'project']).default('global').describe('Installation scope: \'global\' or \'project\''),
    }).strict(),
  }, {
    destructiveHint: false,
    idempotentHint: true,
  });

  console.log(`[Server] Registered 8 tools successfully`);
  return server;
}

/**
 * Main entry point
 */
async function main(): Promise<void> {
  console.log('[Server] Starting OpenCode Skills MCP Server...');

  const server = createServer();

  const transport = new StdioServerTransport();

  try {
    await server.connect(transport);
    console.log('[Server] Server connected and ready, waiting for requests...');
  } catch (error) {
    console.error('[Server] Failed to start server:', error);
    process.exit(1);
  }
}

// Start server if this file is run directly
if (require.main === module) {
  main().catch((error) => {
    console.error('[Server] Fatal error:', error);
    process.exit(1);
  });
}
