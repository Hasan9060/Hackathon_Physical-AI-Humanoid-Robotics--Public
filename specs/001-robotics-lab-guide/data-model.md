# Data Model: Physical AI & Humanoid Robotics Lab Book

**Date**: 2025-12-05
**Phase**: 1 - Design & Data Modeling

## Overview

This document defines the data structures and entities that will be used throughout the Physical AI & Humanoid Robotics Lab book. These models provide the foundation for content organization, code examples, and procurement data.

## Core Content Entities

### Chapter

**Description**: Represents a book chapter with associated metadata and content organization

**Attributes**:
- `chapterId`: Unique identifier (e.g., "01-ros2-fundamentals")
- `title`: Chapter title (string, required)
- `module`: Module identifier (enum: INTRO, ROS2, SIMULATION, AICONTROL, CAPSTONE, HARDWARE)
- `weekCoverage`: Array of week numbers covered (integer[])
- `targetWordCount`: Target word count (integer, required)
- `prerequisites`: Array of prerequisite chapter IDs (string[])
- `learningObjectives`: Array of learning objective strings (string[])
- `contentType`: Content type (enum: MDX, INTERACTIVE, CODE_EXAMPLE)

**Validation Rules**:
- `chapterId` must follow pattern: `{moduleNumber}-{moduleSlug}-{chapterSlug}`
- `targetWordCount` must be between 500 and 2000 words
- `weekCoverage` must be within 1-13 range

### Module

**Description**: Represents a learning module grouping related chapters

**Attributes**:
- `moduleId`: Unique identifier (e.g., "01-ros2")
- `title`: Module title (string, required)
- `description`: Module description (string, required)
- `weeksCovered`: Week range covered (object with `start` and `end` integers)
- `totalWordCount`: Total words across all chapters in module (integer)
- `prerequisites`: Required prior knowledge (string[])

**Available Modules**:
1. **INTRO** - Introduction and Architecture (Weeks 1)
2. **ROS2** - Robot Operating System 2 (Weeks 1-5)
3. **SIMULATION** - Digital Twin and Simulation (Weeks 6-9)
4. **AICONTROL** - AI Control Systems (Weeks 10-12)
5. **CAPSTONE** - VLA and Integration (Week 13)
6. **HARDWARE** - Procurement and Specifications

## Technical Content Entities

### CodeExample

**Description**: Represents executable code examples within chapters

**Attributes**:
- `exampleId`: Unique identifier
- `language`: Programming language (enum: PYTHON, URDF, YAML, BASH)
- `title`: Example title (string, required)
- `description`: Example description (string, required)
- `code`: Actual code content (string, required)
- `explanation`: Step-by-step explanation (string)
- `dependencies`: Required packages or systems (string[])
- `expectedOutput`: Expected execution result (string)
- `chapterReference`: Link to containing chapter (string)

**Code Types**:
- **PYTHON**: ROS 2 rclpy implementations
- **URDF**: Robot model definitions
- **YAML**: Configuration files and launch files
- **BASH**: Setup and installation scripts

### ArchitectureDiagram

**Description**: Represents technical diagrams and illustrations

**Attributes**:
- `diagramId`: Unique identifier
- `title`: Diagram title (string, required)
- `type`: Diagram type (enum: SYSTEM_ARCHITECTURE, DATA_FLOW, HARDWARE_LAYOUT)
- `description`: Diagram description (string, required)
- `components`: Array of diagram components (object[])
- `connections`: Array of component connections (object[])

### ProcurementTable

**Description**: Represents hardware procurement and cost analysis data

**Attributes**:
- `tableId`: Unique identifier
- `title`: Table title (string, required)
- `category`: Table category (enum: WORKSTATION, EDGE_KIT, ROBOT_LAB, SOFTWARE)
- `items`: Array of procurement items (object[])
  - `name`: Item name (string)
  - `specification`: Technical specifications (string)
  - `quantity`: Required quantity (integer)
  - `unitCost`: Cost per unit (number)
  - `totalCost`: Total cost (number)
  - `supplier`: Recommended supplier (string)
  - `alternatives`: Alternative options (string[])
- `totalCost`: Grand total for table (number)
- `currency`: Currency code (string, default: "USD")

## Hardware Specification Entities

### WorkstationSpec

**Description**: Represents Digital Twin Workstation specifications

**Attributes**:
- `component`: Component name (enum: CPU, GPU, RAM, STORAGE, MOTHERBOARD)
- `requirement`: Minimum requirement (string)
- `recommendation`: Recommended specification (string)
- `alternatives`: Alternative options (string[])
- `costRange`: Price range (object with `min` and `max`)
- `vendor`: Recommended vendors (string[])

### EdgeKitSpec

**Description**: Represents Jetson Orin Edge AI Kit specifications

**Attributes**:
- `kitType`: Kit model (enum: ORIN_NANO, ORIN_NX, ORIN_AGX)
- `useCase`: Intended use case (string)
- `performanceClass`: Performance classification (enum: ENTRY, INTERMEDIATE, ADVANCED)
- `keySpecs`: Key specifications (object)
  - `cpu`: CPU specifications
  - `gpu`: GPU specifications
  - `memory`: Memory specifications
  - `storage`: Storage specifications
- `pricePoint`: Price category (enum: BUDGET, STANDARD, PREMIUM)

## Curriculum Mapping Entities

### WeeklyObjective

**Description**: Represents learning objectives for each week

**Attributes**:
- `weekNumber`: Week number (integer, 1-13)
- `title`: Week title (string, required)
- `objectives`: Learning objectives (string[])
- `chapters`: Associated chapters (string[])
- `deliverables`: Student deliverables (string[])
- `assessmentMethods`: Assessment methods (string[])

### LearningPath

**Description**: Represents progressive learning paths through modules

**Attributes**:
- `pathId`: Unique identifier
- `title`: Path title (string, required)
- `description`: Path description (string, required)
- `sequence`: Ordered chapter sequence (string[])
- `prerequisites`: Required prerequisites (string[])
- `outcomes`: Expected learning outcomes (string[])

## Content Relationships

### CrossReference

**Description**: Represents relationships between different content elements

**Attributes**:
- `fromElement`: Source element ID (string)
- `toElement`: Target element ID (string)
- `referenceType`: Type of reference (enum: PREREQUISITE, RELATED, EXAMPLE, IMPLEMENTATION)
- `description`: Description of relationship (string)

## Data Validation Rules

### Content Constraints

1. **Word Count Validation**: Each chapter must stay within ±10% of target word count
2. **Prerequisite Chain**: No circular dependencies in chapter prerequisites
3. **Module Coverage**: All 13 weeks must be covered by at least one chapter
4. **Code Quality**: All code examples must be syntactically valid and tested

### Hardware Specification Validation

1. **Compatibility**: All hardware components must be compatible with each other
2. **Cost Accuracy**: All cost data must include currency and be realistic for current market
3. **Availability**: Recommended components must be commercially available
4. **Performance**: Specifications must meet minimum requirements for curriculum objectives

### Curriculum Validation

1. **Progression**: Learning objectives must show clear progression
2. **Assessment Alignment**: Deliverables must align with learning objectives
3. **Prerequisite Logic**: Prerequisites must be necessary and sufficient
4. **Coverage**: All curriculum requirements must be addressed

## Integration Points

### Docusaurus Integration

The data model integrates with Docusaurus through:

- **Frontmatter**: Chapter metadata stored in MDX frontmatter
- **Sidebar Configuration**: Module and chapter hierarchy drives sidebar generation
- **Component Props**: React components consume data model properties

### Content Generation

Data model enables automated content generation:

- **Structured Data**: Enables programmatic content creation
- **Validation**: Automated validation of content completeness
- **Consistency**: Ensures consistent formatting and structure

## Future Extensions

The data model is designed to accommodate future extensions:

- **Interactive Components**: Support for additional component types
- **Assessment Integration**: Integration with learning management systems
- **Version Management**: Support for curriculum versioning and updates
- **Multi-language**: Support for translations and localization