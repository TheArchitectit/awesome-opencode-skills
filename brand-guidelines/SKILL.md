---
name: brand-guidelines
description: Applies OpenCode's official brand colors and typography to any sort of artifact that may benefit from having OpenCode's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
license: Complete terms in LICENSE.txt
---

# OpenCode Brand Styling

## Overview

To access OpenCode's official brand identity and style resources, use this skill.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, OpenCode brand, visual formatting, visual design

## Brand Guidelines

### Colors

**Main Colors (based on OpenCode default dark theme):**

- **Primary/Dark**: System terminal background (uses "none" - adapts to terminal)
- **Text**: System terminal foreground (uses "none" - adapts to terminal)
- **Primary Accent**: Used for actions and highlights
- **Secondary Accent**: Used for secondary elements
- **Success Green**: Used for success states
- **Error Red**: Used for error states
- **Warning Yellow**: Used for warnings
- **Info Blue**: Used for informational elements

**Recommended Color Palette (for external artifacts):**

When creating artifacts for use outside OpenCode terminal, use these colors:

- **Dark Background**: `#1a1b26` or `#1e1e2e` (based on Nord/dark themes)
- **Light Background**: `#eceff4` or `#d8dee9` (based on Nord light themes)
- **Text (Dark)**: `#d8dee9` or `#eceff4`
- **Text (Light)**: `#2e3440` or `#434c5e`
- **Accent Blue**: `#81a1c1` or `#88c0d0`
- **Accent Green**: `#a3be8c` or `#8fbcbb`
- **Accent Purple**: `#b48ead` or `#d08770`
- **Accent Yellow**: `#ebcb8b` or `#bf616a`

### Typography

- **Headings/Code**: JetBrains Mono, Fira Code, or any modern monospace font
- **Body Text**: System sans-serif (Inter, San Francisco, or equivalent)
- **Note**: Use monospace fonts for code, technical content, and maintain readability with system fonts for general text

## Features

### Smart Font Application

- Applies monospace fonts to code blocks, headings (24pt and larger)
- Applies system sans-serif fonts to body text
- Automatically falls back to system defaults if custom fonts unavailable
- Preserves readability across all systems

### Text Styling

- Code blocks and headings (14pt+): Monospace font
- Body text: System sans-serif font
- Smart color selection based on background (dark/light)
- Preserves text hierarchy and formatting

### Shape and Accent Colors

- Non-text shapes use accent colors from palette
- Cycles through blue, green, purple, and yellow accents
- Maintains visual interest while staying on-brand
- Supports both dark and light modes

## Technical Details

### Font Management

- Uses system-installed JetBrains Mono or Fira Code when available
- Provides automatic fallback to system monospace fonts
- No font installation required - works with existing system fonts
- For best results, install JetBrains Mono or Fira Code in your environment

### Color Application

- Uses RGB color values for precise brand matching
- Applied via python-pptx's RGBColor class or similar
- Maintains color fidelity across different systems
- Supports both dark and light modes

## Usage Guidelines

### When to Use

- Creating presentation slides, reports, or documents
- Designing visual assets or graphics
- Applying consistent styling across multiple artifacts
- Creating branded materials for OpenCode-related content

### Best Practices

- Use monospace fonts for code and technical content
- Apply accent colors sparingly for maximum impact
- Ensure sufficient contrast between text and background
- Consider dark/light mode when choosing colors
- Test color combinations in both light and dark contexts
