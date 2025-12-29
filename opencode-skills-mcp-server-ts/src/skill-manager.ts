/**
 * Skill Manager - Core business logic
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { readdir, copyFile, mkdir, access, rm } from 'fs/promises';
import { 
  initConfig,
  loadSkillsMetadata,
  isSkillInstalled,
  getInstallDir,
  getSkillsDir,
  getCharacterLimit
} from './config.js';

// Workflow combinations
const WORKFLOW_COMBINATIONS = {
  'content-pipeline': {
    name: 'Content Creation Pipeline',
    description: 'Create professional blog posts with images and branding',
    skills: ['content-research-writer', 'image-enhancer', 'canvas-design', 'brand-guidelines'],
    category: 'Writing'
  },
  'product-launch': {
    name: 'Product Launch Workflow',
    description: 'Complete product launch preparation from domain to documentation',
    skills: [
      'domain-name-brainstormer', 'competitive-ads-extractor',
      'lead-research-assistant', 'content-research-writer',
      'artifacts-builder', 'theme-factory', 'changelog-generator'
    ],
    category: 'Business'
  },
  'development-cycle': {
    name: 'Developer Productivity Cycle',
    description: 'Daily development workflow - testing, documentation, organization',
    skills: ['webapp-testing', 'changelog-generator', 'skill-creator', 'file-organizer'],
    category: 'Development'
  },
  'document-workflow': {
    name: 'Professional Document Workflow',
    description: 'Create professional business documents with proper formatting',
    skills: ['docx', 'pdf', 'image-enhancer', 'brand-guidelines', 'internal-comms'],
    category: 'Document Processing'
  },
  'visual-campaign': {
    name: 'Visual Marketing Campaign',
    description: 'Create marketing assets with consistent branding',
    skills: [
      'canvas-design', 'theme-factory', 'image-enhancer',
      'brand-guidelines', 'slack-gif-creator'
    ],
    category: 'Visual'
  }
};

export async function listSkills(options: {
  category?: string;
  depth?: string;
  installedOnly?: boolean;
} = {}): Promise<string> {
  const metadata = await loadSkillsMetadata();
  
  let filteredMetadata = { ...metadata };

  if (options.category) {
    filteredMetadata = Object.fromEntries(
      Object.entries(filteredMetadata).filter(([_, v]: [string, any]) => v.category === options.category)
    );
  }

  if (options.depth) {
    filteredMetadata = Object.fromEntries(
      Object.entries(filteredMetadata).filter(([_, v]: [string, any]) => v.depth === options.depth)
    );
  }

  if (options.installedOnly) {
    const installed: Record<string, boolean> = {};
    for (const [skillName] of Object.keys(filteredMetadata)) {
      installed[skillName] = await isSkillInstalled(skillName);
    }
    filteredMetadata = Object.fromEntries(
      Object.entries(filteredMetadata).filter(([k]: [string, any]) => installed[k])
    );
  }

  if (Object.keys(filteredMetadata).length === 0) {
    return '# Skills\n\nNo skills found matching your criteria.';
  }

  let result = '# Available OpenCode Skills\n\n';

  for (const [skillName, skillData] of Object.entries(filteredMetadata)) {
    const isInstalled = await isSkillInstalled(skillName);
    const installedMark = isInstalled ? ' ✅' : '';
    const depthIcon = skillData.depth === 'Comprehensive' ? '📖' : '📄';

    result += `## ${depthIcon} ${skillName}${installedMark}\n\n`;
    result += `**Description**: ${skillData.description}\n\n`;
    result += `**Category**: ${skillData.category}\n\n`;
    result += `**Depth**: ${skillData.depth}\n\n`;
    result += `**Lines**: ${skillData.lines}\n\n`;
    result += `**Prerequisites**: ${skillData.prerequisites}\n\n`;
    result += '---\n\n';
  }

  const characterLimit = getCharacterLimit();
  if (result.length > characterLimit) {
    result = result.slice(0, characterLimit) + '\n\n[Output truncated due to length limit]';
  }

  return result;
}

export async function getSkillInfo(skillName: string): Promise<string> {
  const metadata = await loadSkillsMetadata();

  if (!(skillName in metadata)) {
    return `# Error\n\nSkill '${skillName}' not found. Use list_skills to see available skills.`;
  }

  const skillData = metadata[skillName];
  const isInstalled = await isSkillInstalled(skillName);
  const installedStatus = isInstalled ? '✅ Installed' : '⬜ Not installed';

  let result = `# ${skillName}\n\n`;
  result += `**Status**: ${installedStatus}\n\n`;
  result += `**Description**: ${skillData.description}\n\n`;
  result += `**Category**: ${skillData.category}\n\n`;
  result += `**Depth**: ${skillData.depth}\n\n`;
  result += `**Documentation Lines**: ${skillData.lines}\n\n`;
  result += `**Prerequisites**:\n\`\`\`\n${skillData.prerequisites}\n\`\`\`\n\n`;
  result += `**Keywords**: ${skillData.keywords.join(', ')}\n\n`;

  if (isInstalled) {
    const installDir = getInstallDir('global');
    result += `**Location**: ${path.join(installDir, skillName)}\n\n`;
  }

  return result;
}

export async function installSkill(skillName: string, scope: 'global' | 'project' = 'global'): Promise<string> {
  const metadata = await loadSkillsMetadata();

  if (!(skillName in metadata)) {
    return `# Error\n\nSkill '${skillName}' not found. Use list_skills to see available skills.`;
  }

  const installDir = getInstallDir(scope);
  const skillsDir = getSkillsDir();
  const skillPath = path.join(skillsDir, skillName);
  const destPath = path.join(installDir, skillName);

  // Check if skill exists
  try {
    await access(skillPath);
  } catch {
    return `# Error\n\nSkill directory '${skillName}' not found in skills directory.`;
  }

  // Check if already installed
  try {
    await access(destPath);
    return `# Installation Skipped\n\nSkill '${skillName}' is already installed at ${destPath}`;
  } catch {
    // Not installed, proceed
  }

  try {
    // Create destination directory if needed
    await mkdir(installDir, { recursive: true });

    // Recursively copy skill directory
    await copyDirectory(skillPath, destPath);

    const skillData = metadata[skillName];
    let result = `✅ Successfully installed '${skillName}'\n\n`;
    result += `**Location**: ${destPath}\n`;
    result += `**Scope**: ${scope}\n\n`;
    result += `**Prerequisites**: ${skillData.prerequisites}\n\n`;
    result += 'Note: Restart OpenCode to load the new skill.';

    return result;
  } catch (error) {
    return `# Error\n\n❌ Failed to install '${skillName}': ${error}`;
  }
}

async function copyDirectory(src: string, dest: string): Promise<void> {
  // Create destination
  await mkdir(dest, { recursive: true });

  // Read source directory
  const entries = await readdir(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath2 = path.join(dest, entry.name);

    if (entry.isDirectory) {
      // Recursively copy subdirectories
      await copyDirectory(srcPath, destPath2);
    } else {
      // Copy files
      await copyFile(srcPath, destPath2);
    }
  }
}

export async function uninstallSkill(skillName: string, scope: 'global' | 'project' = 'global'): Promise<string> {
  const installDir = getInstallDir(scope);
  const skillPath = path.join(installDir, skillName);

  try {
    await access(skillPath);
  } catch {
    return `# Error\n\nSkill '${skillName}' is not installed.`;
  }

  try {
    await rm(skillPath, { recursive: true, force: true });

    let result = `✅ Successfully uninstalled '${skillName}'\n\n`;
    result += `**Location removed**: ${skillPath}\n`;
    result += 'Note: Restart OpenCode to update the skill list.';

    return result;
  } catch (error) {
    return `# Error\n\n❌ Failed to uninstall '${skillName}': ${error}`;
  }
}

export async function searchSkills(query: string): Promise<string> {
  const metadata = await loadSkillsMetadata();
  const queryLower = query.toLowerCase();

  const matches: [string, any][] = [];

  for (const [skillName, skillData] of Object.entries(metadata)) {
    const description = skillData.description.toLowerCase();
    const keywords = skillData.keywords.map((k: string) => k.toLowerCase());
    const category = skillData.category.toLowerCase();

    if (
      queryLower.includes(description) ||
      keywords.some((k: string) => queryLower.includes(k)) ||
      queryLower.includes(category) ||
      queryLower.includes(skillName.toLowerCase())
    ) {
      matches.push([skillName, skillData]);
    }
  }

  if (matches.length === 0) {
    return `# Search Results\n\nNo skills found matching '${query}'. Try different keywords.`;
  }

  let result = `# Search Results for '${query}'\n\n`;

  for (const [skillName, skillData] of matches) {
    const isInstalled = await isSkillInstalled(skillName);
    const installedMark = isInstalled ? ' ✅' : '';
    result += `## ${skillName}${installedMark}\n\n`;
    result += `**Category**: ${skillData.category}\n\n`;
    result += `**Description**: ${skillData.description}\n\n`;
    result += '---\n\n';
  }

  const characterLimit = getCharacterLimit();
  if (result.length > characterLimit) {
    result = result.slice(0, characterLimit) + '\n\n[Output truncated due to length limit]';
  }

  return result;
}

export async function validateSkill(skillPathStr: string): Promise<string> {
  const skillPath = path.resolve(skillPathStr);
  const skillMd = path.join(skillPath, 'SKILL.md');

  try {
    await access(skillMd);
  } catch {
    return `# Validation Error\n\nSKILL.md not found at ${skillMd}`;
  }

  try {
    const content = await fs.readFile(skillMd, 'utf-8');
  } catch (error) {
    return `# Validation Error\n\nFailed to read SKILL.md: ${error}`;
  }

  // Check for YAML frontmatter
  if (!content.startsWith('---')) {
    return '# Validation Error\n\n❌ Invalid: Missing YAML frontmatter (must start with \'---\')';
  }

  // Check for closing ---
  const frontmatterEnd = content.indexOf('---', 3);
  if (frontmatterEnd === -1) {
    return '# Validation Error\n\n❌ Invalid: Missing closing \'---\' in YAML frontmatter';
  }

  const frontmatter = content.slice(0, frontmatterEnd);

  // Check for required fields
  const requiredFields = ['name', 'description'];
  const missingFields = requiredFields.filter((field: string) => !frontmatter.includes(field));

  if (missingFields.length > 0) {
    return `# Validation Error\n\n❌ Invalid: Missing required YAML fields: ${missingFields.join(', ')}`;
  }

  // Check skill name format
  const nameMatch = frontmatter.match(/name:\s*(.+)/);
  if (nameMatch) {
    const skillName = nameMatch[1].trim();
    if (skillName.includes(' ') || !/^[a-z0-9-]+$/.test(skillName)) {
      return `# Validation Error\n\n❌ Invalid: Skill name '${skillName}' should be hyphen-case (no spaces, lowercase letters, numbers, hyphens)`;
    }
  }

  return '# Validation Result\n\n✅ Valid: Skill SKILL.md structure is correct';
}

export async function getCombinations(category?: string): Promise<string> {
  let combinations = { ...WORKFLOW_COMBINATIONS };

  if (category) {
    combinations = Object.fromEntries(
      Object.entries(combinations).filter(([_, v]: [string, any]) => v.category === category)
    );
  }

  if (Object.keys(combinations).length === 0) {
    return '# Skill Combinations\n\nNo combinations found matching your criteria.';
  }

  let result = '# Recommended Skill Combinations\n\n';

  for (const [comboKey, comboData] of Object.entries(combinations)) {
    result += `## ${comboData.name}\n\n`;
    result += `**Description**: ${comboData.description}\n\n`;
    result += `**Category**: ${comboData.category}\n\n`;
    result += `**Skills**: ${comboData.skills.join(', ')}\n\n`;

    // Check which skills are installed
    const installed: string[] = [];
    const missing: string[] = [];

    for (const skillName of comboData.skills) {
      if (await isSkillInstalled(skillName)) {
        installed.push(skillName);
      } else {
        missing.push(skillName);
      }
    }

    if (installed.length > 0) {
      result += `**Already installed**: ${installed.join(', ')}\n\n`;
    }
    if (missing.length > 0) {
      result += `**Need to install**: ${missing.join(', ')}\n\n`;
    }

    result += `**Install workflow**: \`install_workflow --workflow-name ${comboKey}\`\n\n`;
    result += '---\n\n';
  }

  const characterLimit = getCharacterLimit();
  if (result.length > characterLimit) {
    result = result.slice(0, characterLimit) + '\n\n[Output truncated due to length limit]';
  }

  return result;
}

export async function installWorkflow(workflowName: string, scope: 'global' | 'project' = 'global'): Promise<string> {
  if (!(workflowName in WORKFLOW_COMBINATIONS)) {
    return `# Error\n\nWorkflow '${workflowName}' not found. Use get_combinations to see available workflows.`;
  }

  const workflow = WORKFLOW_COMBINATIONS[workflowName as keyof typeof WORKFLOW_COMBINATIONS];
  const skillsToInstall = workflow.skills;
  const installDir = getInstallDir(scope);
  const skillsDir = getSkillsDir();

  // Create install directory
  await mkdir(installDir, { recursive: true });

  let result = `# Installing '${workflow.name}' Workflow\n\n`;
  result += `**Scope**: ${scope}\n\n`;
  result += '**Skills to install**:\n\n';

  let installedCount = 0;
  let failedCount = 0;

  for (const skillName of skillsToInstall) {
    const skillPath = path.join(skillsDir, skillName);
    const destPath = path.join(installDir, skillName);

    result += `- ${skillName}: `;

    try {
      await access(destPath);
      result += '⚠️  Already installed\n';
      installedCount++;
    } catch {
      // Not installed, try to copy
      try {
        await access(skillPath);
        await copyDirectory(skillPath, destPath);
        result += '✅ Installed\n';
        installedCount++;
      } catch {
        result += '❌ Not found in skills directory\n';
        failedCount++;
      }
    }
  }

  result += `\n**Summary**: ${installedCount} installed, ${failedCount} failed\n\n`;
  result += 'Note: Restart OpenCode to load new skills.';

  return result;
}
