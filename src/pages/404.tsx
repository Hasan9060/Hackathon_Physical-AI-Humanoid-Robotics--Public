import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './404.module.css';

export default function Custom404(): JSX.Element {
  return (
    <Layout>
      <div className={styles.custom404}>
        <div className={styles.robot404}>
          <div className={styles.robotAnimation}>
            <div className={styles.robotHead}>
              <div className={styles.robotEye}></div>
              <div className={styles.robotEye}></div>
              <div className={styles.robotMouth}>😕</div>
            </div>
            <div className={styles.robotBody}>
              <div className={styles.robotArm + ' ' + styles.leftArm}>🦾</div>
              <div className={styles.robotChest}>
                <span className={styles.errorCode}>404</span>
              </div>
              <div className={styles.robotArm + ' ' + styles.rightArm}>🦾</div>
            </div>
            <div className={styles.robotLegs}>
              <div className={styles.robotLeg + ' ' + styles.leftLeg}></div>
              <div className={styles.robotLeg + ' ' + styles.rightLeg}></div>
            </div>
          </div>
        </div>

        <div className={styles.content}>
          <h1 className={styles.title}>
            Oops! This Circuit is Broken
          </h1>
          <p className={styles.description}>
            It looks like you've wandered into uncharted territory in our robotics lab.
            The page you're looking for seems to have lost its connection to our main system.
          </p>
          <p className={styles.subDescription}>
            But don't worry! Our comprehensive <strong>Physical AI & Humanoid Robotics</strong>
            curriculum has everything you need to master the art of building intelligent robots.
          </p>

          <div className={styles.suggestions}>
            <h3>You might be looking for:</h3>
            <div className={styles.suggestionLinks}>
              <Link to="/" className={styles.suggestionLink}>
                <span className={styles.linkIcon}>🏠</span>
                <div className={styles.linkContent}>
                  <span className={styles.linkTitle}>Home</span>
                  <span className={styles.linkDesc}>Start your robotics journey</span>
                </div>
              </Link>

              <Link to="/intro/overview" className={styles.suggestionLink}>
                <span className={styles.linkIcon}>📋</span>
                <div className={styles.linkContent}>
                  <span className={styles.linkTitle}>Course Overview</span>
                  <span className={styles.linkDesc}>Explore the complete curriculum</span>
                </div>
              </Link>

              <Link to="/ros2/fundamentals" className={styles.suggestionLink}>
                <span className={styles.linkIcon}>🔧</span>
                <div className={styles.linkContent}>
                  <span className={styles.linkTitle}>ROS 2 Fundamentals</span>
                  <span className={styles.linkDesc}>Begin with the basics</span>
                </div>
              </Link>

              <Link to="/simulation/gazebo-setup" className={styles.suggestionLink}>
                <span className={styles.linkIcon}>🌍</span>
                <div className={styles.linkContent}>
                  <span className={styles.linkTitle}>Simulation</span>
                  <span className={styles.linkDesc}>Build digital twins</span>
                </div>
              </Link>

              <Link to="/hardware/workstation-spec" className={styles.suggestionLink}>
                <span className={styles.linkIcon}>💻</span>
                <div className={styles.linkContent}>
                  <span className={styles.linkTitle}>Hardware Guide</span>
                  <span className={styles.linkDesc}>Set up your lab infrastructure</span>
                </div>
              </Link>
            </div>
          </div>

          <div className={styles.actions}>
            <Link to="/" className={styles.primaryButton}>
              <span>🚀</span>
              Start Reading the Book
            </Link>
            <Link to="/intro/architecture-overview" className={styles.secondaryButton}>
              <span>🏗️</span>
              View Architecture
            </Link>
          </div>
        </div>

        <div className={styles.floatingElements}>
          <div className={styles.gear + ' ' + styles.gear1}>⚙️</div>
          <div className={styles.gear + ' ' + styles.gear2}>⚙️</div>
          <div className={styles.gear + ' ' + styles.gear3}>⚙️</div>
          <div className={styles.circuit1}>🔌</div>
          <div className={styles.circuit2}>💡</div>
          <div className={styles.circuit3}>🔋</div>
          <div className={styles.circuit4}>📡</div>
        </div>
      </div>
    </Layout>
  );
}