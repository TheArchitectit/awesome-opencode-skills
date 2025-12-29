# OpenCode Skill Interactions Guide

This guide explains how different skills work together to accomplish complex tasks. Skills are designed to complement each other, not just exist in isolation.

## How Skills Interact

OpenCode can load multiple skills simultaneously when they're relevant to a task. Skills interact by:

1. **Context Sharing**: One skill's output becomes input for another
2. **Sequential Processing**: Skills execute in a logical order (research → write → format)
3. **Parallel Execution**: Multiple skills work simultaneously on different aspects
4. **Tool Coordination**: Skills share tools and resources efficiently

## Common Skill Combinations

### 1. Content Creation Pipeline

**Use Case**: Create a professional blog post with images

**Skill Sequence**:
```
1. content-research-writer - Research and write article
2. image-enhancer - Improve screenshots for the article
3. canvas-design - Create custom graphics/illustrations
4. brand-guidelines - Apply consistent styling to all visuals
5. internal-comms - Write announcement for sharing the post
```

**Why This Works**:
- content-research-writer provides citations and structure
- image-enhancer ensures visuals are sharp
- canvas-design creates unique branded graphics
- brand-guidelines maintains consistency across all assets
- internal-comms formats announcement in company style

### 2. Product Launch Workflow

**Use Case**: Launching a new product or feature

**Skill Sequence**:
```
1. domain-name-brainstormer - Find domain name for product
2. competitive-ads-extractor - Research competitor messaging
3. lead-research-assistant - Identify target customers
4. content-research-writer - Write landing page copy
5. artifacts-builder - Build branded landing page artifact
6. theme-factory - Apply professional theme
7. changelog-generator - Create release notes
```

**Why This Works**:
- Domain brainstorming establishes brand identity
- Competitive research informs positioning
- Lead research identifies target audience
- Content writing creates compelling copy
- Artifacts builder turns copy into interactive demo
- Theme factory ensures professional presentation
- Chelog generator provides release documentation

### 3. Developer Productivity Cycle

**Use Case**: Managing daily development workflow

**Skill Sequence**:
```
1. webapp-testing - Test new features
2. changelog-generator - Document changes
3. skill-creator - Create custom skill for repetitive tasks
4. file-organizer - Keep project files organized
5. developer-growth-analysis - Review patterns and get learning resources
```

**Why This Works**:
- Testing ensures quality before commits
- Changelog documents progress systematically
- Skill creator automates repetitive workflows
- File organizer maintains clean project structure
- Growth analysis provides personalized feedback

### 4. Professional Document Workflow

**Use Case**: Creating professional business documents

**Skill Sequence**:
```
1. docx - Create or edit Word document
2. pdf - Convert or annotate PDF version
3. image-enhancer - Enhance any screenshots/graphics
4. brand-guidelines - Apply company branding
5. internal-comms - Format as internal communication
```

**Why This Works**:
- docx handles tracked changes for collaboration
- pdf provides readonly format for distribution
- Image enhancer ensures visuals are sharp
- Brand guidelines maintain consistency
- Internal comms ensures proper format

### 5. Visual Marketing Campaign

**Use Case**: Creating marketing assets

**Skill Sequence**:
```
1. canvas-design - Create visual assets (posters, graphics)
2. theme-factory - Apply theme color palette
3. image-enhancer - Enhance resolution/quality
4. brand-guidelines - Apply brand colors/fonts
5. slack-gif-creator - Create animated versions for Slack
6. internal-comms - Write campaign announcement
```

**Why This Works**:
- Canvas design creates original visuals
- Theme factory ensures color consistency
- Image enhancer improves final quality
- Brand guidelines enforce corporate identity
- Slack GIF creator creates engaging animations
- Internal comms formats announcements properly

### 6. Research & Reporting

**Use Case**: Comprehensive research report

**Skill Sequence**:
```
1. competitive-ads-extractor - Analyze competitor strategies
2. lead-research-assistant - Identify target companies
3. content-research-writer - Write research report with citations
4. pptx - Create presentation slides
5. theme-factory - Apply professional theme
6. brand-guidelines - Style with company branding
```

**Why This Works**:
- Competitive analysis provides market context
- Lead research identifies potential customers
- Content writer structures report with evidence
- PPTX creates visual presentation
- Theme and brand skills ensure professional appearance

### 7. Organization & Cleanup

**Use Case**: Organizing project files and resources

**Skill Sequence**:
```
1. file-organizer - Clean up project directory
2. invoice-organizer - Organize project-related invoices
3. mcp-builder - Create custom MCP server for project tools
4. skill-creator - Document workflows as new skills
5. changelog-generator - Generate changelog for organized state
```

**Why This Works**:
- File organizer creates logical structure
- Invoice organizer handles financial documents
- MCP builder automates project-specific tools
- Skill creator captures team knowledge
- Chelog generator documents the organization effort

### 8. Meeting & Communication

**Use Case**: Improving team communication

**Skill Sequence**:
```
1. meeting-insights-analyzer - Analyze communication patterns
2. content-research-writer - Write improvement suggestions
3. internal-comms - Format as team feedback
4. domain-name-brainstormer - Brainstorm initiative names
5. changelog-generator - Document action items
```

**Why This Works**:
- Meeting insights provides data-driven feedback
- Content writer structures recommendations
- Internal comms formats appropriately for team
- Domain brainstorming aids in naming initiatives
- Chelog tracks implementation of improvements

### 9. Personal Productivity

**Use Case**: Managing personal projects and finances

**Skill Sequence**:
```
1. file-organizer - Organize documents and files
2. invoice-organizer - Sort invoices for taxes
3. content-research-writer - Write personal project documentation
4. developer-growth-analysis - Get personalized learning recommendations
5. raffle-winner-picker - Run contests or giveaways (if applicable)
```

**Why This Works**:
- File organizer reduces digital clutter
- Invoice organizer handles tax preparation
- Content writer creates clear documentation
- Growth analysis provides tailored learning path
- Raffle picker handles fair selection (optional)

### 10. Technical Documentation

**Use Case**: Creating technical documentation

**Skill Sequence**:
```
1. content-research-writer - Research best practices
2. skill-creator - Document as reusable skill
3. docx - Create user-facing documentation
4. pdf - Generate technical specification PDF
5. webapp-testing - Verify examples work correctly
6. changelog-generator - Document what changed
```

**Why This Works**:
- Research ensures accuracy and best practices
- Skill creator captures knowledge for reuse
- Docx provides editable format
- PDF creates spec for distribution
- Testing validates examples
- Chelog tracks documentation updates

## Skill Interaction Patterns

### Sequential Processing

Skills execute one after another, where each output feeds the next:

```
Task: "Create a marketing email"
└── content-research-writer (research and write)
    └── internal-comms (format as company email)
```

### Parallel Processing

Multiple skills work simultaneously on different aspects:

```
Task: "Prepare launch materials"
├── domain-name-brainstormer (find domain)
├── competitive-ads-extractor (research competitors)
├── lead-research-assistant (identify leads)
└── content-research-writer (write copy)
    └── All outputs feed into artifacts-builder (create landing page)
```

### Conditional Activation

Skills load only when their specific conditions are met:

```
Task: "Help with my PDF forms"
├── pdf skill loads (for general PDF work)
└── IF forms detected → specialized form-filling workflow activates
```

### Iterative Refinement

Skills cycle back through each other for improvement:

```
Task: "Perfect this presentation"
├── pptx (create slides)
├── theme-factory (apply theme)
├── brand-guidelines (apply branding)
├── image-enhancer (enhance graphics)
└── Loop back to pptx for refinements based on visual quality
```

## Best Practices for Skill Combinations

### 1. Start Simple, Add Complexity

Begin with one skill, then add others as needed:
```
# Start simple
content-research-writer

# Add more
content-research-writer → image-enhancer → brand-guidelines
```

### 2. Understand Skill Outputs

Know what each skill produces before chaining:
- **content-research-writer**: Markdown with citations
- **canvas-design**: PNG/PDF visual assets
- **artifacts-builder**: HTML artifacts
- **docx/pptx**: Word/PowerPoint files

### 3. Use Explicit Instructions

Guide OpenCode on how to combine skills:
```
"Use content-research-writer to research and write, then apply brand-guidelines to any visuals"
```

### 4. Iterate and Refine

Skills work best with feedback:
```
"Review this with canvas-design, then enhance with image-enhancer, 
and finally apply brand-guidelines"
```

### 5. Leverage Automation

Skills that create new skills (skill-creator) amplify effectiveness:
```
"Use skill-creator to capture this workflow, so we can reuse it"
```

## Avoiding Conflicts

### Resource Conflicts

Some skills access similar resources - be explicit about priorities:

```
"First, use image-enhancer to improve this screenshot, 
then apply canvas-design effects"
```

### Output Overwrites

Be clear about which skill's output to keep:

```
"Apply theme-factory to color palette, but keep canvas-design's composition"
```

### Tool Collisions

Some skills use similar tools - specify order:

```
"Use webapp-testing first to verify functionality, 
then create artifacts with artifacts-builder"
```

## Advanced Skill Orchestration

### Complex Multi-Stage Projects

For large projects, plan skill sequence ahead:

```
Stage 1 (Planning):
- domain-name-brainstormer
- competitive-ads-extractor
- lead-research-assistant

Stage 2 (Creation):
- content-research-writer
- artifacts-builder
- canvas-design

Stage 3 (Testing):
- webapp-testing
- file-organizer

Stage 4 (Launch):
- changelog-generator
- internal-comms
```

### Skill Libraries

Create reusable skill combinations for your workflows:

```
# Define as skill library
My Blog Post Workflow:
1. content-research-writer
2. image-enhancer
3. brand-guidelines

# Use it
"Use my blog post workflow for this topic"
```

### Custom Skill Compositions

Use skill-creator to package skill combinations:

```
"Create a new skill that combines: lead-research-assistant, 
competitive-ads-extractor, and content-research-writer"
```

## Measuring Success

Track how well skills work together:

### Effectiveness Metrics

- **Time saved**: How much faster vs. manual?
- **Quality**: Is output better than using skills individually?
- **Learning curve**: How quickly can you reuse combinations?
- **Reliability**: Do skills conflict or fail together?

### Optimization Patterns

Monitor and improve:

1. **Identify bottlenecks** - Which skill slows down workflow?
2. **Find redundancies** - Do skills duplicate effort?
3. **Sequence optimization** - Reorder for efficiency?
4. **Skill selection** - Are there better skill alternatives?

## Examples in Action

### Example 1: Launching a SaaS Feature

**Request**: "Help me launch our new analytics dashboard"

**Skill Sequence**:
```
1. competitive-ads-extractor
   → Research how competitors position analytics features

2. lead-research-assistant
   → Identify companies that would benefit from this feature

3. content-research-writer
   → Write launch announcement with research-backed claims

4. pptx
   → Create demo slides deck

5. theme-factory
   → Apply professional "tech innovation" theme

6. brand-guidelines
   → Style with our company colors

7. changelog-generator
   → Generate release notes

8. internal-comms
   → Write internal announcement
```

**Result**: Complete launch package - research, messaging, demo, release notes, announcements.

### Example 2: Creating a Case Study

**Request**: "Turn this project into a compelling case study"

**Skill Sequence**:
```
1. content-research-writer
   → Research project background and industry trends

2. file-organizer
   → Gather project artifacts, screenshots, data

3. image-enhancer
   → Enhance all visuals for publication quality

4. content-research-writer
   → Write case study narrative with data points

5. docx
   → Create professional case study document

6. pdf
   → Generate PDF version for distribution

7. brand-guidelines
   → Apply consistent styling throughout
```

**Result**: Polished, research-backed case study ready for publication.

### Example 3: Weekly Team Update

**Request**: "Help me prepare our weekly team update"

**Skill Sequence**:
```
1. changelog-generator
   → Generate changelog from this week's commits

2. content-research-writer
   → Synthesize into compelling narrative

3. meeting-insights-analyzer
   → Add insights from recent team meetings

4. internal-comms
   → Format in company update template

5. slack-gif-creator (optional)
   → Create fun GIF celebrating wins
```

**Result**: Professional, data-driven team update with visuals and engagement.

## Getting Started with Skill Combinations

### Beginner Combinations

Start with these simple 2-skill combinations:

1. **Writing + Branding**:
   ```
   content-research-writer + brand-guidelines
   ```

2. **Organization + Changelog**:
   ```
   file-organizer + changelog-generator
   ```

3. **Research + Documentation**:
   ```
   competitive-ads-extractor + content-research-writer
   ```

### Intermediate Combinations

Try these 3-4 skill workflows:

1. **Full Content Pipeline**:
   ```
   content-research-writer + image-enhancer + canvas-design + brand-guidelines
   ```

2. **Launch Preparation**:
   ```
   domain-name-brainstormer + lead-research-assistant + artifacts-builder + theme-factory
   ```

3. **Development Cycle**:
   ```
   webapp-testing + changelog-generator + skill-creator + file-organizer
   ```

### Advanced Combinations

Master these complex workflows:

1. **Complete Product Launch**:
   ```
   All research skills + all creation skills + all communication skills
   ```

2. **Automated Workflow Creation**:
   ```
   Use skill-creator to package skill combinations for reuse
   ```

3. **Team Productivity Suite**:
   ```
   All communication + organization + development skills
   ```

## Summary

- Skills are designed to work together, not alone
- Understand what each skill outputs before combining
- Use explicit instructions to guide skill sequencing
- Iterate and refine combinations for your needs
- Package successful combinations as new skills
- Track effectiveness and optimize over time

The more you understand how skills interact, the more powerful OpenCode becomes for your workflows.
