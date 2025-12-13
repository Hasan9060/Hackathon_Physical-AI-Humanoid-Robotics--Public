import React, { useState, useEffect } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './styles.module.css';

export default function ScrollProgress() {
  const { colorMode } = useDocusaurusContext();
  const [scrollProgress, setScrollProgress] = useState(0);
  const [isVisible, setIsVisible] = useState(false);
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

    // Initial detection
    detectTheme();

    // Listen for theme changes
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

  useEffect(() => {
    const calculateScrollProgress = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight;
      const winHeight = window.innerHeight;
      const scrollPercent = scrollTop / (docHeight - winHeight);
      const scrollPercentRounded = Math.round(scrollPercent * 100);

      setScrollProgress(scrollPercentRounded);

      // Show progress bar only after scrolling a bit
      setIsVisible(scrollTop > 100);
    };

    const handleScroll = () => {
      requestAnimationFrame(calculateScrollProgress);
    };

    // Initial calculation
    calculateScrollProgress();

    // Add scroll event listener
    window.addEventListener('scroll', handleScroll, { passive: true });

    // Cleanup
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    {/* Progress bar at the top of the page only */}
    <div
      className={`${styles.progressBar} ${isVisible ? styles.visible : ''} ${isDarkMode ? styles.dark : styles.light}`}
      style={{ width: `${scrollProgress}%` }}
    />
  );
}