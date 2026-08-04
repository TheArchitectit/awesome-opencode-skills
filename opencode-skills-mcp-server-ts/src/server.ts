/**
 * MCP Server - Main entry point
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { 
  StdioServerTransport 
} from '@modelcontextprotocol/sdk/server/stdio.js';
import { fileURLToPath } from 'url';
import { z } from 'zod';

import {
  listSkills,
  getSkillInfo,
  installSkill,
  uninstallSkill,
  searchSkills,
  validateSkill,
  getCombinations,
  installWorkflow
} from './skill-manager.js';

/**
 * Create and configure MCP server with all tools registered
 */
export function createServer(): McpServer {
  console.log('[Server] Creating OpenCode Skills MCP Server...');

  const server = new McpServer(
    {
      name: 'opencode-skills-mcp',
      version: '1.0.0',
    },
    {
      capabilities: {},
    }
  );

  console.log('[Server] Registering tools...');

  server.registerTool('list_skills', {
    description: 'List all available OpenCode skills with optional filtering by category or depth. Shows installation status.',
    inputSchema: {
      category: z.string().optional().describe('Filter by skill category (e.g., \'Development\', \'Writing\', \'Document Processing\')'),
      depth: z.string().optional().describe('Filter by depth (e.g., \'Comprehensive\', \'Standard\', \'Quick Reference\')'),
      installed_only: z.boolean().optional().default(false).describe('Only show installed skills'),
    },
  }, async ({ category, depth, installed_only }) => {
    const result = await listSkills({ category, depth, installedOnly: installed_only });
    return { content: [{ type: 'text', text: result }] };
  });

  server.registerTool('get_skill_info', {
    description: 'Get detailed information about a specific OpenCode skill including description, prerequisites, and installation status.',
    inputSchema: {
      skill_name: z.string().describe('Name of the skill to get information about'),
    },
  }, async ({ skill_name }) => {
    const result = await getSkillInfo(skill_name);
    return { content: [{ type: 'text', text: result }] };
  });

  server.registerTool('install_skill', {
    description: 'Install an OpenCode skill globally or locally to your project. Automatically handles file copying.',
    inputSchema: {
      skill_name: z.string().describe('Name of the skill to install'),
      scope: z.enum(['global', 'project']).default('global').describe('Installation scope: \'global\' or \'project\''),
    },
    annotations: {
      destructiveHint: false,
      idempotentHint: true,
    },
  }, async ({ skill_name, scope }) => {
    const result = await installSkill(skill_name, scope);
    return { content: [{ type: 'text', text: result }] };
  });

  server.registerTool('uninstall_skill', {
    description: 'Uninstall an OpenCode skill from global or local installation directory.',
    inputSchema: {
      skill_name: z.string().describe('Name of the skill to uninstall'),
      scope: z.enum(['global', 'project']).default('global').describe('Uninstallation scope: \'global\' or \'project\''),
    },
    annotations: {
      destructiveHint: true,
    },
  }, async ({ skill_name, scope }) => {
    const result = await uninstallSkill(skill_name, scope);
    return { content: [{ type: 'text', text: result }] };
  });

  server.registerTool('search_skills', {
    description: 'Search for OpenCode skills by keywords, description, or category name.',
    inputSchema: {
      query: z.string().describe('Search query (keywords or description)'),
    },
    annotations: {
      readOnlyHint: true,
    },
  }, async ({ query }) => {
    const result = await searchSkills(query);
    return { content: [{ type: 'text', text: result }] };
  });

  server.registerTool('validate_skill', {
    description: 'Validate a skill\'s SKILL.md file structure for proper YAML frontmatter and required fields.',
    inputSchema: {
      skill_path: z.string().describe('Path to the skill directory to validate'),
    },
    annotations: {
      readOnlyHint: true,
    },
  }, async ({ skill_path }) => {
    const result = await validateSkill(skill_path);
    return { content: [{ type: 'text', text: result }] };
  });

  server.registerTool('get_combinations', {
    description: 'Get recommended skill combinations and workflows with installation status for each skill.',
    inputSchema: {
      category: z.string().optional().describe('Filter by workflow category (e.g., \'Writing\', \'Development\', \'Business\')'),
    },
    annotations: {
      readOnlyHint: true,
    },
  }, async ({ category }) => {
    const result = await getCombinations(category);
    return { content: [{ type: 'text', text: result }] };
  });

  server.registerTool('install_workflow', {
    description: 'Install all skills for a recommended workflow combination (e.g., content-pipeline, product-launch).',
    inputSchema: {
      workflow_name: z.string().describe('Name of the workflow to install (e.g., \'content-pipeline\', \'product-launch\', \'development-cycle\')'),
      scope: z.enum(['global', 'project']).default('global').describe('Installation scope: \'global\' or \'project\''),
    },
    annotations: {
      destructiveHint: false,
      idempotentHint: true,
    },
  }, async ({ workflow_name, scope }) => {
    const result = await installWorkflow(workflow_name, scope);
    return { content: [{ type: 'text', text: result }] };
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

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    console.error('[Server] Fatal error:', error);
    process.exit(1);
  });
}
