/**
 * OpenCode Skills MCP Server - Entry Point
 */

import { fileURLToPath } from 'url';
import { createServer } from './server.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { initConfig } from './config.js';

export { createServer } from './server.js';
export * from './skill-manager.js';
export * from './config.js';

async function main(): Promise<void> {
  initConfig();
  const server = createServer();
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    console.error('[Server] Fatal error:', error);
    process.exit(1);
  });
}
