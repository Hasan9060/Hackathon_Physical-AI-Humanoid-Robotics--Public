import React, { useEffect, useRef, useState } from 'react';
import styles from './styles.module.css';

interface Dot {
  id: number;
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
}

const AnimatedDotsBackground: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationFrameRef = useRef<number>();
  const mouseRef = useRef({ x: -1000, y: -1000 });
  const dotsRef = useRef<Dot[]>([]);
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const resizeCanvas = () => {
      const rect = canvas.parentElement?.getBoundingClientRect();
      if (rect) {
        canvas.width = rect.width;
        canvas.height = rect.height;
      } else {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
      }
      console.log('Canvas size:', canvas.width, canvas.height);
      initDots();
    };

    const initDots = () => {
      const numberOfDots = Math.max(20, Math.floor((canvas.width * canvas.height) / 25000));
      dotsRef.current = [];

      for (let i = 0; i < numberOfDots; i++) {
        dotsRef.current.push({
          id: i,
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          vx: (Math.random() - 0.5) * 0.3,
          vy: (Math.random() - 0.5) * 0.3,
          radius: Math.random() * 1.5 + 0.5, // Smaller dots (0.5 - 2px)
        });
      }
    };

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      mouseRef.current = {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
      };
    };

    const handleMouseLeave = () => {
      mouseRef.current = { x: -1000, y: -1000 };
    };

    const drawDot = (dot: Dot) => {
      ctx.beginPath();
      ctx.arc(dot.x, dot.y, dot.radius, 0, Math.PI * 2);
      ctx.fillStyle = isDarkMode ? 'rgba(236, 72, 153, 0.8)' : 'rgba(236, 72, 153, 0.6)';
      ctx.fill();
    };

    const drawConnections = () => {
      for (let i = 0; i < dotsRef.current.length; i++) {
        for (let j = i + 1; j < dotsRef.current.length; j++) {
          const dot1 = dotsRef.current[i];
          const dot2 = dotsRef.current[j];
          const distance = Math.sqrt(
            Math.pow(dot1.x - dot2.x, 2) + Math.pow(dot1.y - dot2.y, 2)
          );

          if (distance < 120) {
            const opacity = 1 - distance / 120;
            const lineOpacity = isDarkMode ? opacity * 0.3 : opacity * 0.2;
            ctx.strokeStyle = `rgba(236, 72, 153, ${lineOpacity})`;
            ctx.lineWidth = 0.5;
            ctx.beginPath();
            ctx.moveTo(dot1.x, dot1.y);
            ctx.lineTo(dot2.x, dot2.y);
            ctx.stroke();
          }
        }
      }
    };

    const updateDots = () => {
      dotsRef.current.forEach((dot) => {
        // Mouse repulsion effect
        const dx = dot.x - mouseRef.current.x;
        const dy = dot.y - mouseRef.current.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 100) {
          const force = (100 - distance) / 100;
          const angle = Math.atan2(dy, dx);
          dot.vx += Math.cos(angle) * force * 0.5;
          dot.vy += Math.sin(angle) * force * 0.5;
        }

        // Apply friction
        dot.vx *= 0.98;
        dot.vy *= 0.98;

        // Update position
        dot.x += dot.vx;
        dot.y += dot.vy;

        // Bounce off walls
        if (dot.x < 0 || dot.x > canvas.width) {
          dot.vx = -dot.vx;
          dot.x = Math.max(0, Math.min(canvas.width, dot.x));
        }
        if (dot.y < 0 || dot.y > canvas.height) {
          dot.vy = -dot.vy;
          dot.y = Math.max(0, Math.min(canvas.height, dot.y));
        }

        // Add some random movement
        dot.vx += (Math.random() - 0.5) * 0.1;
        dot.vy += (Math.random() - 0.5) * 0.1;

        // Limit maximum velocity
        const maxSpeed = 2;
        const currentSpeed = Math.sqrt(dot.vx * dot.vx + dot.vy * dot.vy);
        if (currentSpeed > maxSpeed) {
          dot.vx = (dot.vx / currentSpeed) * maxSpeed;
          dot.vy = (dot.vy / currentSpeed) * maxSpeed;
        }
      });
    };

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      updateDots();
      drawConnections();
      dotsRef.current.forEach(drawDot);

      animationFrameRef.current = requestAnimationFrame(animate);
    };

    // Check initial theme
    const checkTheme = () => {
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark' ||
                     (!document.documentElement.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
      setIsDarkMode(isDark);
    };

    // Theme change observer
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
          checkTheme();
        }
      });
    });

    resizeCanvas();
    checkTheme();
    observer.observe(document.documentElement, { attributes: true });
    window.addEventListener('resize', resizeCanvas);
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('mouseleave', handleMouseLeave);
    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      canvas.removeEventListener('mousemove', handleMouseMove);
      canvas.removeEventListener('mouseleave', handleMouseLeave);
      observer.disconnect();
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [isDarkMode]);

  return (
    <canvas
      ref={canvasRef}
      className={styles.canvas}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: 0
      }}
    />
  );
};

export default AnimatedDotsBackground;