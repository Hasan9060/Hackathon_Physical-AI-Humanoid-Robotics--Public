---
# Prompt History Record (PHR)

id: "002"
title: "Docusaurus Spec-Kit Constitution"
stage: "constitution"
date_iso: "2025-12-05"
surface: "agent"
model: "claude-4.5-sonnet"
feature: "none"
branch: "master"
user: "claude-code"
command: "/sp.constitution"
labels: ["constitution", "docusaurus", "spec-kit", "ci-cd", "technical-book"]

# Links
spec: null
ticket: null
adr: null
pr: null

# Content Generation
files_yaml:
  - .specify/memory/constitution.md

tests_yaml: []
---

## Prompt Text (verbatim)

/sp.constitution

Project: AI-Driven Technical Book using Docusaurus & Spec-Kit Plus

Core principles:

Spec-Driven Architecture: All content generation starts with Spec-Kit Plus definitions.

Documentation-as-Code: Treat book content as software (versioned, modular, tested).

Docusaurus-Native: Adhere strictly to Docusaurus routing, sidebars, and MDX component standards.

CI/CD Deployment: Automated publishing to GitHub Pages via GitHub Actions.

Key standards:

File Format: MDX (Markdown + React) with valid frontmatter.

Directory Structure: Hierarchical organization within the /docs folder.

Navigation: Explicit configuration in sidebars.js for chapter ordering.

Styling: Use Docusaurus admonitions (::note, ::tip) for emphasis; avoid inline HTML styles.

Writing Style: Clear, concise technical English (Google Developer Style Guide).

Reference Management: Hyperlinks for internal navigation; standard citations for external data.

Constraints:

Generator: Claude Code CLI.

Framework: Docusaurus v3+.

Hosting: GitHub Pages (requires correct baseUrl and url in config).

Output: Static HTML build.

Plagiarism: 0% tolerance; original synthesis of verified specs.

Success criteria:

Functional Docusaurus site deployed live on GitHub Pages.

npm run build completes with zero errors.

Sidebar navigation accurately reflects the book structure.

All Spec-Kit Plus .sp files are preserved in the repository for reproducibility.

Content passes readability checks (technical concepts explained clearly).

## Response Text

Successfully updated project constitution for AI-Driven Technical Book using Docusaurus & Spec-Kit Plus with:

**New version**: 2.0.0 (major version - complete project pivot)
**Core principles updated**: 4 principles focused on Spec-Kit Plus, Documentation-as-Code, Docusaurus-Native, and CI/CD Deployment
**Technical standards defined**: MDX format, directory structure, navigation, styling, and writing standards
**Framework constraints**: Docusaurus v3+, GitHub Pages hosting, static HTML output, 0% plagiarism tolerance
**Governance framework**: Automated deployment, quality assurance, and release management procedures

**Key files updated**:
- `.specify/memory/constitution.md` - Complete constitution with technical standards and CI/CD requirements

**Success criteria defined**:
- Functional Docusaurus site on GitHub Pages
- Zero build errors
- Accurate sidebar navigation
- Preserved Spec-Kit Plus files
- Readable technical content

**Next steps**: Template consistency review and Docusaurus project setup

## Outcome

Successfully pivoted project constitution from AI/robotics textbook (v1.0.0) to AI-driven technical book using Docusaurus & Spec-Kit Plus (v2.0.0). The new constitution establishes modern documentation-as-code practices with automated deployment, strict technical standards, and reproducible content generation workflows.

## Evaluation

- Constitution completed with complete project direction pivot
- All 6 previous principles replaced with 4 new Docusaurus/Spec-Kit Plus focused principles
- Major version bump (2.0.0) reflects fundamental change in project scope
- Technical standards defined for MDX, directory structure, navigation, and CI/CD
- Quality gates established with zero-error build requirements
- Template consistency identified as follow-up requirement