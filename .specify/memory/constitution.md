<!-- Sync Impact Report:
- Version change: 1.0.0 → 2.0.0 (major - complete project pivot)
- Modified principles: All 6 principles replaced with Docusaurus/Spec-Kit Plus focused principles
- Added sections: CI/CD Deployment standards
- Removed sections: Ethics/Safety requirements (not applicable to technical documentation)
- Templates requiring updates: ⚠ All template files need consistency review
- Follow-up TODOs: Set up Docusaurus project structure and GitHub Actions workflow
-->

# AI-Driven Technical Book using Docusaurus & Spec-Kit Plus Constitution

## Core Principles

### Spec-Driven Architecture
All content generation starts with Spec-Kit Plus definitions. Every chapter, section, and component must be traceable to specification files. Content must not be created independently of specifications. Rationale: Ensures reproducibility and maintains consistency across the entire book.

### Documentation-as-Code
Treat book content as software with version control, modular architecture, and automated testing. Every change must go through standard software development practices. Rationale: Enables collaboration, maintains quality, and allows for reliable deployment.

### Docusaurus-Native
Adhere strictly to Docusaurus routing, sidebars, and MDX component standards. No custom routing logic or non-standard component usage. Rationale: Ensures compatibility, maintainability, and leverages Docusaurus's built-in features.

### CI/CD Deployment
Automated publishing to GitHub Pages via GitHub Actions. No manual deployment steps. Rationale: Eliminates human error, ensures consistent builds, and provides rapid feedback loops.

## Key Standards

### File Format
- MDX (Markdown + React) with valid frontmatter
- All content files must include proper metadata
- React components must follow Docusaurus plugin standards

### Directory Structure
- Hierarchical organization within the /docs folder
- Clear separation between content, assets, and configuration
- Logical grouping by chapters and sections

### Navigation
- Explicit configuration in sidebars.js for chapter ordering
- All pages must be discoverable through navigation
- No orphan pages or broken links

### Styling
- Use Docusaurus admonitions (::note, ::tip) for emphasis
- Avoid inline HTML styles
- Maintain consistent formatting across all content

### Writing Style
- Clear, concise technical English (Google Developer Style Guide)
- Technical concepts explained clearly
- Proper grammar and consistent terminology

### Reference Management
- Hyperlinks for internal navigation
- Standard citations for external data
- All links must be functional and relevant

## Constraints

### Generator
- Claude Code CLI only
- No other content generation tools permitted

### Framework
- Docusaurus v3+ strictly
- No forked or modified versions

### Hosting
- GitHub Pages only
- Requires correct baseUrl and url in configuration

### Output
- Static HTML build only
- No server-side rendering or dynamic content

### Plagiarism
- 0% tolerance
- Original synthesis of verified specs required
- All sources must be properly credited

## Governance

### Amendment Process
- This constitution supersedes all other project guidelines
- Amendments require documentation and approval
- All content must comply with principles before publication
- Technical changes require testing in staging environment

### Quality Assurance
- All content must pass MDX validation
- Build process must complete with zero errors
- Navigation structure must be functional
- All spec files must be preserved

### Development Workflow
- Content follows spec-driven development process
- Regular automated testing of build process
- Version control with clear change documentation
- Continuous integration and deployment

### Release Management
- Automated deployment via GitHub Actions
- Manual intervention only for emergency fixes
- All releases must be tagged and documented
- Rollback procedures documented and tested

**Version**: 2.0.0 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-05