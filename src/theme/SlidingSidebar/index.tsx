import React, { useState, useEffect } from 'react';
import { useLocation } from '@docusaurus/router';
import './styles.css';

export default function SlidingSidebar(): JSX.Element {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  // Close sidebar when route changes
  useEffect(() => {
    setIsOpen(false);
  }, [location.pathname]);

  // Toggle sidebar
  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  // Close sidebar when clicking overlay
  const handleOverlayClick = () => {
    setIsOpen(false);
  };

  // Close sidebar on escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setIsOpen(false);
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, []);

  return (
    <>
      {/* Sidebar Toggle Button */}
      <button
        className={`sidebar-toggle ${isOpen ? 'active' : ''}`}
        onClick={toggleSidebar}
        aria-label={isOpen ? 'Close sidebar' : 'Open sidebar'}
        aria-expanded={isOpen}
      >
        <div className="hamburger">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </button>

      {/* Sidebar Container */}
      <aside className={`sidebar-container ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-content">
          <div className="sidebar-header">
            <h2 className="sidebar-title">Navigation</h2>
            <p className="sidebar-subtitle">Quick access to curriculum modules</p>
          </div>

          <nav className="sidebar-nav">
            <div className="sidebar-nav-item">
              <a href="/" className="sidebar-nav-link">
                <span className="sidebar-nav-icon">🏠</span>
                <span>Home</span>
              </a>
            </div>

            <div className="sidebar-nav-item">
              <a href="/intro/overview" className="sidebar-nav-link">
                <span className="sidebar-nav-icon">📋</span>
                <span>Overview</span>
              </a>
            </div>

            <div className="sidebar-nav-item">
              <a href="/intro/architecture-overview" className="sidebar-nav-link">
                <span className="sidebar-nav-icon">🏗️</span>
                <span>Architecture</span>
              </a>
            </div>

            <div className="sidebar-nav-item">
              <a href="/intro/hardware-requirements" className="sidebar-nav-link">
                <span className="sidebar-nav-icon">⚙️</span>
                <span>Hardware Requirements</span>
              </a>
            </div>

            <div className="sidebar-nav-item">
              <span className="sidebar-nav-link" style={{ color: 'var(--ifm-color-primary-light)', fontWeight: 600 }}>
                <span className="sidebar-nav-icon">📚</span>
                <span>Module 1: ROS 2</span>
              </span>
            </div>

            <div className="sidebar-nav-item">
              <a href="/ros2/fundamentals" className="sidebar-nav-link">
                <span className="sidebar-nav-icon">🔧</span>
                <span>ROS 2 Fundamentals</span>
              </a>
            </div>

            <div className="sidebar-nav-item">
              <a href="/ros2/rclpy-implementation" className="sidebar-nav-link">
                <span className="sidebar-nav-icon">🐍</span>
                <span>rclpy Implementation</span>
              </a>
            </div>

            <div className="sidebar-nav-item">
              <a href="/ros2/urdf-and-robot-modeling" className="sidebar-nav-link">
                <span className="sidebar-nav-icon">🤖</span>
                <span>URDF & Robot Modeling</span>
              </a>
            </div>

            <div className="sidebar-nav-item">
              <span className="sidebar-nav-link" style={{ color: 'var(--ifm-color-primary-light)', fontWeight: 600 }}>
                <span className="sidebar-nav-icon">🎮</span>
                <span>Module 2: Simulation</span>
              </span>
            </div>

            <div className="sidebar-nav-item">
              <a href="/simulation/gazebo-setup" className="sidebar-nav-link">
                <span className="sidebar-nav-icon">🌍</span>
                <span>Gazebo Setup</span>
              </a>
            </div>

            <div className="sidebar-nav-item">
              <a href="/simulation/sensor-modeling" className="sidebar-nav-link">
                <span className="sidebar-nav-icon">📡</span>
                <span>Sensor Modeling</span>
              </a>
            </div>

            <div className="sidebar-nav-item">
              <a href="/simulation/unity-visualization" className="sidebar-nav-link">
                <span className="sidebar-nav-icon">🎨</span>
                <span>Unity Visualization</span>
              </a>
            </div>

            <div className="sidebar-nav-item">
              <span className="sidebar-nav-link" style={{ color: 'var(--ifm-color-primary-light)', fontWeight: 600 }}>
                <span className="sidebar-nav-icon">🧠</span>
                <span>Module 3: AI Control</span>
              </span>
            </div>

            <div className="sidebar-nav-item">
              <a href="/aicontrol/isaac-sim-setup" className="sidebar-nav-link">
                <span className="sidebar-nav-icon">🚀</span>
                <span>Isaac Sim Setup</span>
              </a>
            </div>

            <div className="sidebar-nav-item">
              <a href="/aicontrol/sim-to-real-transfer" className="sidebar-nav-link">
                <span className="sidebar-nav-icon">🔄</span>
                <span>Sim-to-Real Transfer</span>
              </a>
            </div>

            <div className="sidebar-nav-item">
              <a href="/aicontrol/humanoid-kinematics" className="sidebar-nav-link">
                <span className="sidebar-nav-icon">🚶</span>
                <span>Humanoid Kinematics</span>
              </a>
            </div>

            <div className="sidebar-nav-item">
              <span className="sidebar-nav-link" style={{ color: 'var(--ifm-color-primary-light)', fontWeight: 600 }}>
                <span className="sidebar-nav-icon">💻</span>
                <span>Hardware Procurement</span>
              </span>
            </div>

            <div className="sidebar-nav-item">
              <a href="/hardware/workstation-spec" className="sidebar-nav-link">
                <span className="sidebar-nav-icon">🖥️</span>
                <span>Workstation Specs</span>
              </a>
            </div>

            <div className="sidebar-nav-item">
              <a href="/hardware/procurement-tables" className="sidebar-nav-link">
                <span className="sidebar-nav-icon">📊</span>
                <span>Procurement Tables</span>
              </a>
            </div>

            <div className="sidebar-nav-item">
              <a href="https://github.com/hasanrafay/humanoid-robotics-textbook" className="sidebar-nav-link" target="_blank" rel="noopener noreferrer">
                <span className="sidebar-nav-icon">🔗</span>
                <span>GitHub Repository</span>
              </a>
            </div>
          </nav>
        </div>
      </aside>

      {/* Overlay */}
      <div
        className={`sidebar-overlay ${isOpen ? 'active' : ''}`}
        onClick={handleOverlayClick}
        aria-hidden={!isOpen}
      />
    </>
  );
}