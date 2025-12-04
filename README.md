# Physical AI & Humanoid Robotics Lab Book

A comprehensive 14,000-word technical guide for academic institutions planning and implementing Physical AI & Humanoid Robotics labs.

## Overview

This book provides detailed technical architecture and procurement guidance for setting up a "Physical AI & Humanoid Robotics" curriculum. It covers:

- **13-week curriculum structure** with dedicated chapters for each technical module
- **Three core infrastructure components**: Digital Twin Workstation, Edge AI Kit, Robot Lab
- **On-Premise vs Cloud-Native analysis** with detailed cost justification
- **Sim-to-Real transfer concepts** and hardware dependencies

## Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn package manager

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd humanoid-robotics-textbook

# Install dependencies
npm install

# Start development server
npm start
```

### Build

```bash
# Build static site
npm build

# Serve built site locally
npm serve
```

## Project Structure

```
docs/                          # Docusaurus content
├── 00-intro/                 # Introduction modules
├── 01-ros2/                  # ROS 2 fundamentals
├── 02-simulation/            # Digital twin and simulation
├── 03-aicontrol/             # AI control systems
├── 04-capstone/              # VLA and integration
└── 99-hardware/              # Procurement and specifications

src/                          # React components and customization
├── components/               # Reusable components
├── theme/                    # Docusaurus theme overrides
└── css/                      # Custom styling

specs/                        # Specification documents
└── 001-robotics-lab-guide/   # Feature specifications

static/                       # Static assets
└── img/                      # Images and diagrams
```

## Content Organization

### Module Structure

1. **Introduction & Architecture** (Weeks 1)
2. **ROS 2 Fundamentals** (Weeks 1-5)
3. **Digital Twin & Simulation** (Weeks 6-9)
4. **AI Control Systems** (Weeks 10-12)
5. **VLA & Capstone** (Week 13)

### Target Audience

- Academic leaders and Robotics Program Directors
- Technical professionals responsible for lab planning
- Procurement specialists for educational infrastructure

## Development

### Adding New Content

1. Create MDX files in appropriate `docs/` subdirectory
2. Include proper frontmatter with title, description, and metadata
3. Use React components for interactive elements
4. Test with `npm start` before committing

### Styling

- Use Tailwind CSS for component styling
- Follow Docusaurus theming conventions
- Maintain consistency across modules

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Docusaurus](https://docusaurus.io/)
- Spec-driven development using [Spec-Kit Plus](https://spec-kit.plus/)
- Content generated with Claude Code CLI