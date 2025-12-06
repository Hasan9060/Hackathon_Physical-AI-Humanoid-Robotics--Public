import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import AnimatedDotsBackground from '@site/src/components/AnimatedDotsBackground';

import styles from './index.module.css';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <AnimatedDotsBackground />
      <div className="container">
        <div className={styles.heroContent}>
          <div className={styles.heroLeft}>
            <div className={styles.bookCoverContainer}>
              <img
                src="img/book-cover.png"
                alt="Physical AI & Humanoid Robotics Lab - Book Cover"
                className={styles.bookCover}
                loading="eager"
                decoding="sync"
                style={{
                  imageRendering: 'auto',
                  WebkitImageRendering: 'auto'
                }}
              />
            </div>
          </div>
          <div className={styles.heroRight}>
            <h1 className="hero__title">{siteConfig.title}</h1>
            <p className="hero__subtitle">{siteConfig.tagline}</p>
            <div className={styles.buttons}>
              <Link
                className="button button--primary button--lg"
                to="/intro/overview">
                Start Reading
              </Link>
              <Link
                className="button button--secondary button--lg"
                to="/hardware/workstation-spec">
                Hardware Requirements
              </Link>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}