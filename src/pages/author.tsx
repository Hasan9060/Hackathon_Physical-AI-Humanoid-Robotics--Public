import React from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './author.module.css';

export default function Author() {
    const { siteConfig } = useDocusaurusContext();

    return (
        <Layout
            title="About the Author"
            description="About Syed Hasan Rafay, author of the Humanoid Robotics Textbook">
            <main className={styles.authorContainer}>
                <div className={styles.authorCard}>
                    <div className={styles.imageContainer}>
                        <img
                            src="/img/author.png"
                            alt="Syed Hasan Rafay"
                            className={styles.authorImage}
                        />
                    </div>

                    <div className={styles.contentContainer}>
                        <h1 className={styles.authorName}>Syed Hasan Rafay</h1>
                        <div className={styles.badges}>
                            <span className={styles.badge}>AI Agentic Developer</span>
                            <span className={styles.badge}>Book author</span>
                            <span className={styles.badge}>GIAIC</span>
                        </div>

                        <div className={styles.educationCard}>
                            <h3>Hackathon AI Driven</h3>
                            <p>
                                Currently pursuing advanced AI studies at <strong>GIAIC (Governor Sindh Initiative for AI, Web 3.0 & Metaverse)</strong>.
                            </p>
                            <ul className={styles.detailsList}>
                                <li><strong>Slot:</strong> Saturday ( 2 to 5 Evening)</li>
                                <li><strong>Teachers:</strong> Sir Ali Aftab & Sir Hamza</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </main>
        </Layout>
    );
}
