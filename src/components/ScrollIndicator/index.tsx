import React, { useState, useEffect } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './styles.module.css';

export default function ScrollIndicator() {
  const [scrollProgress, setScrollProgress] = useState(0);
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Theme detection
  useEffect(() => {
    const detectTheme = () => {
      const htmlElement = document.documentElement;
      const isDark = htmlElement.classList.contains('dark') ||
                    htmlElement.getAttribute('data-theme') === 'dark' ||
                    window.matchMedia('(prefers-color-scheme: dark)').matches;
      setIsDarkMode(isDark);
    };

    detectTheme();

    const observer = new MutationObserver(() => {
      detectTheme();
    });

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class', 'data-theme'],
      childList: false,
      subtree: false
    });

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addListener(detectTheme);

    return () => {
      observer.disconnect();
      mediaQuery.removeListener(detectTheme);
    };
  }, []);

  // Scroll tracking
  useEffect(() => {
    const calculateScrollProgress = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight;
      const winHeight = window.innerHeight;
      const scrollPercent = scrollTop / (docHeight - winHeight);
      const scrollPercentRounded = Math.round(scrollPercent * 100);

      setScrollProgress(scrollPercentRounded);
    };

    const handleScroll = () => {
      requestAnimationFrame(calculateScrollProgress);
    };

    calculateScrollProgress();
    window.addEventListener('scroll', handleScroll, { passive: true });

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <div className={styles.scrollIndicator}>
      {/* Track background */}
      <div className={`${styles.track} ${isDarkMode ? styles.dark : styles.light}`} />

      {/* Progress fill */}
      <div
        className={`${styles.progress} ${isDarkMode ? styles.dark : styles.light}`}
        style={{ width: `${scrollProgress}%` }}
      />

      {/* Glow effect at end of progress */}
      {scrollProgress > 0 && (
        <div
          className={`${styles.glow} ${isDarkMode ? styles.dark : styles.light}`}
          style={{ left: `${scrollProgress}%` }}
        />
      )}
    </div>
  );
}