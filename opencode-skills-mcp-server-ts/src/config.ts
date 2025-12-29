/**
 * OpenCode Skills MCP Server - Configuration
 */

import * as fs from 'fs/promises';
import * as path from 'path';

// Configuration constants
const CHARACTER_LIMIT = 25000;

// Paths
let SKILLS_DIR: string;
let OPENCODE_GLOBAL: string;
let OPENCODE_PROJECT: string;

export function initConfig(customSkillsDir?: string): void {
  // Auto-detect skills directory
  SKILLS_DIR = customSkillsDir || path.resolve(__dirname, '..', '..');

  // OpenCode installation paths
  const HOME = process.env.HOME || process.env.USERPROFILE;
  OPENCODE_GLOBAL = path.join(HOME, '.config', 'opencode', 'skill');
  OPENCODE_PROJECT = path.join(process.cwd(), '.opencode', 'skill');

  console.log(`[Config] Initialized skills_dir: ${SKILLS_DIR}`);
}

export function getSkillsDir(): string {
  return SKILLS_DIR;
}

export function getSkillsMetadataPath(): string {
  return path.join(SKILLS_DIR, 'skills_metadata.json');
}

export function getInstallDir(scope: 'global' | 'project' = 'global'): string {
  return scope === 'project' ? OPENCODE_PROJECT : OPENCODE_GLOBAL;
}

export async function loadSkillsMetadata(): Promise<Record<string, SkillMetadata>> {
  const metadataPath = getSkillsMetadataPath();
  
  try {
    const data = await fs.readFile(metadataPath, 'utf-8');
    const metadata = JSON.parse(data) as Record<string, SkillMetadata>;
    console.log(`[Config] Loaded metadata for ${Object.keys(metadata).length} skills`);
    return metadata;
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
      console.warn(`[Config] Skills metadata file not found: ${metadataPath}`);
      return {};
    }
    console.error(`[Config] Error loading skills metadata:`, error);
    return {};
  }
}

export async function isSkillInstalled(skillName: string, scope: 'global' | 'project' = 'global'): Promise<boolean> {
  const installDir = getInstallDir(scope);
  const skillPath = path.join(installDir, skillName);

  try {
    await fs.access(skillPath);
    const skillMd = path.join(skillPath, 'SKILL.md');
    const isInstalled = (await fs.access(skillMd).then(() => true).catch(() => false));
    console.log(`[Config] Skill '${skillName}' installed: ${isInstalled} (scope: ${scope})`);
    return isInstalled;
  } catch {
    return false;
  }
}

export function getCharacterLimit(): number {
  return CHARACTER_LIMIT;
}

export interface SkillMetadata {
  name: string;
  description: string;
  category: string;
  depth: string;
  lines: number;
  keywords: string[];
  prerequisites: string;
}
