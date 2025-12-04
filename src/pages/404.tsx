import React from 'react';
import Layout from '@theme/Layout';
import NotFound from '@theme/NotFound';
import styles from './404.module.css';

export default function Custom404(): JSX.Element {
  return (
    <Layout>
      <div className={styles.custom404}>
        <NotFound />
        <div className={styles.actions}>
          <a href="/" className="button button--primary">
            Go Home
          </a>
          <a href="/docs/welcome" className="button button--secondary">
            Start Learning
          </a>
        </div>
      </div>
    </Layout>
  );
}