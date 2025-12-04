# Quickstart Guide: Physical AI & Humanoid Robotics Lab Book

**Purpose**: Rapid setup and validation of the book development environment
**Target Audience**: Development team and content contributors
**Last Updated**: 2025-12-05

## Prerequisites

### System Requirements
- Node.js 18+ (for Docusaurus build system)
- Git (for version control)
- Text editor with MDX support (VS Code recommended)

### Development Environment Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd humanoid-robotics-textbook
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Start Development Server**
   ```bash
   npm run start
   ```

4. **Validate Setup**
   - Open http://localhost:3000
   - Verify all navigation links work
   - Check MDX compilation succeeds

## Content Creation Workflow

### 1. Chapter Template

Create new MDX files using this frontmatter template:

```mdx
---
title: "Chapter Title"
description: "Chapter description"
sidebar_label: "Chapter Display Name"
slug: "/path/to/chapter"
authors: [{name: "Author Name"}]
tags: ["ros2", "simulation", "hardware"]
---

# Chapter Title

Content here with proper structure...
```

### 2. Content Structure Guidelines

- **Headers**: Use `##` for section headers, `###` for subsections
- **Code Blocks**: Specify language for syntax highlighting
- **Images**: Store in `static/img/` directory
- **Links**: Use relative paths for internal links

### 3. Word Count Management

- Target word counts specified in `plan.md`
- Use word count tools to track progress
- Adjust content depth based on word count targets

### 4. Code Example Standards

```python
# Python code example
import rclpy
from rclpy.node import Node

class ExampleNode(Node):
    def __init__(self):
        super().__init__('example_node')
        # Implementation here
```

- Always include language specification
- Provide explanation before and after code blocks
- Test code examples for syntax validity

## File Organization

### Directory Structure
```
docs/
├── 00-intro/           # Introduction and overview
├── 01-ros2/           # ROS 2 fundamentals and implementation
├── 02-simulation/     # Simulation and digital twin
├── 03-aicontrol/      # AI control systems
├── 04-capstone/       # VLA and integration projects
└── 99-hardware/       # Hardware specifications and procurement
```

### Naming Conventions
- **Files**: kebab-case (e.g., `fundamentals.mdx`)
- **Directories**: two-digit prefixes for ordering (e.g., `01-ros2/`)
- **Images**: descriptive names with chapter prefix (e.g., `ros2-node-graph.png`)

## Quality Assurance Checklist

### Content Review
- [ ] Chapter follows assigned structure
- [ ] Word count within ±10% of target
- [ ] All code examples are tested
- [ ] Cross-references are accurate
- [ ] Tables and figures are properly labeled

### Technical Validation
- [ ] MDX compiles without errors
- [ ] All internal links resolve correctly
- [ ] Images load properly
- [ ] Code blocks have correct syntax highlighting
- [ ] Navigation structure is accurate

### Build Validation
```bash
# Test build process
npm run build

# Check for broken links
npm run build 2>&1 | grep -i "warn\|error"

# Validate MDX syntax
npm run build 2>&1 | grep -i "failed"
```

## Development Workflow

### 1. Feature Branch Development
```bash
# Create feature branch
git checkout -b feature/chapter-01-ros2

# Make changes
# ...

# Commit changes
git add .
git commit -m "feat: add ROS 2 fundamentals chapter"

# Push and create PR
git push origin feature/chapter-01-ros2
```

### 2. Content Review Process
1. **Self-Review**: Use checklist above
2. **Peer Review**: Request review from team member
3. **Technical Review**: Validate technical accuracy
4. **Final Approval**: Merge to main branch

### 3. Continuous Integration
- **Build Validation**: Automated on each commit
- **Link Checking**: Automated on each PR
- **Content Validation**: Manual during review process

## Common Issues and Solutions

### MDX Compilation Errors
**Issue**: Invalid JSX syntax in MDX
**Solution**: Check for unclosed tags, invalid attributes, or missing imports

### Image Loading Issues
**Issue**: Images not displaying correctly
**Solution**: Ensure images are in `static/` directory and use correct relative paths

### Link Validation Errors
**Issue**: Broken internal links
**Solution**: Verify file paths and update cross-references

### Build Performance Issues
**Issue**: Slow build times
**Solution**: Limit inline React components, optimize images, check for circular dependencies

## Resources and References

### Documentation
- [Docusaurus Documentation](https://docusaurus.io/)
- [MDX Documentation](https://mdxjs.com/)
- [MDX Code Block Options](https://docusaurus.io/docs/markdown-features/code-blocks)

### Tools
- [VS Code MDX Extension](https://marketplace.visualstudio.com/items?itemName=unifiedjs.vscode-mdx)
- [Word Count Tools](https://wordcounter.net/)
- [Markdown Linter](https://github.com/DavidAnson/markdownlint)

### Style Guide
- Follow Google Developer Documentation Style Guide
- Use active voice and clear, concise language
- Define technical terms on first use
- Maintain consistent terminology throughout

## Support

For questions or issues:
1. Check existing documentation
2. Review similar chapters for consistency
3. Contact the development team
4. Create GitHub issue for technical problems

Remember: This is a living document. Update it as processes evolve and new best practices emerge.