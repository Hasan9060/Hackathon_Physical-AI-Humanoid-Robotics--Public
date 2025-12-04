import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'welcome',
      label: 'Welcome to the Physical AI Lab',
    },
    {
      type: 'doc',
      id: 'architecture-overview',
      label: 'High-Level Infrastructure Architecture',
    },
    {
      type: 'category',
      label: 'Module 1: Introduction & Architecture',
      collapsible: true,
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'intro/welcome',
          label: 'Welcome to the Physical AI Lab',
        },
        {
          type: 'doc',
          id: 'intro/architecture-overview',
          label: 'High-Level Infrastructure Architecture',
        },
        {
          type: 'doc',
          id: 'intro/hardware-requirements',
          label: 'Hardware Requirements and Specifications',
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 2: ROS 2 Fundamentals',
      collapsible: true,
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'ros2/fundamentals',
          label: 'ROS 2 Fundamentals: Core Concepts',
        },
        {
          type: 'doc',
          id: 'ros2/rclpy-implementation',
          label: 'Python Implementation with rclpy',
        },
        {
          type: 'doc',
          id: 'ros2/urdf-and-robot-modeling',
          label: 'URDF: Defining Robot Kinematics and Visuals',
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 3: Simulation & Digital Twin',
      collapsible: true,
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'simulation/gazebo-setup',
          label: 'Gazebo Classic & Ignition Setup and Bridge',
        },
        {
          type: 'doc',
          id: 'simulation/sensor-modeling',
          label: 'Simulating Sensors (LiDAR, IMU, Camera)',
        },
        {
          type: 'doc',
          id: 'simulation/unity-visualization',
          label: 'Advanced Visualization with Unity',
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 4: AI Control Systems',
      collapsible: true,
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'aicontrol/isaac-sim-setup',
          label: 'NVIDIA Isaac Sim: Core Environment',
        },
        {
          type: 'doc',
          id: 'aicontrol/sim-to-real-transfer',
          label: 'Sim-to-Real Transfer Techniques',
        },
        {
          type: 'doc',
          id: 'aicontrol/humanoid-kinematics',
          label: 'Humanoid Kinematics and Bipedal Locomotion',
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 5: VLA & Capstone',
      collapsible: true,
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'capstone/vla-conversational-ai',
          label: 'Vision-Language-Action (VLA) Architecture',
        },
        {
          type: 'doc',
          id: 'capstone/final-project-breakdown',
          label: 'Capstone Project: Full Stack Integration',
        },
      ],
    },
    {
      type: 'category',
      label: 'Hardware Procurement',
      collapsible: true,
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'hardware/workstation-spec',
          label: 'Workstation & Edge Kit Requirements',
        },
        {
          type: 'doc',
          id: 'hardware/procurement-tables',
          label: 'Lab Procurement & Cost Analysis',
        },
      ],
    },
  ],
};

export default sidebars;