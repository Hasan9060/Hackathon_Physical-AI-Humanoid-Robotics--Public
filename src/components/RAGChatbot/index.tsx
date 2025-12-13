import React, { useState, useEffect, useRef } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './styles.module.css';
import { ChatMessage, ChatSource } from './types';

interface RAGChatbotProps {
  apiBaseUrl?: string;
  sessionId?: string;
  onSessionChange?: (sessionId: string) => void;
}

export function RAGChatbot({
  apiBaseUrl = 'http://localhost:8000/api/v1',
  sessionId: initialSessionId,
  onSessionChange
}: RAGChatbotProps) {
  const { colorMode } = useDocusaurusContext();
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [sessionId, setSessionId] = useState(initialSessionId || '');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [showTextSelection, setShowTextSelection] = useState(false);
  const [isTyping, setIsTyping] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

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

    // Observe changes to html element class and attributes
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class', 'data-theme'],
      childList: false,
      subtree: false
    });

    // Listen for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addListener(detectTheme);

    return () => {
      observer.disconnect();
      mediaQuery.removeListener(detectTheme);
    };
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load session history if sessionId provided
  useEffect(() => {
    if (sessionId) {
      loadSessionHistory();
    }
  }, [sessionId]);

  // Handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection?.toString().trim();

      // Only show selection if text is meaningful (at least 5 characters)
      if (text && text.length > 5) {
        // Don't show selection for whitespace-only or very common single words
        const isMeaningfulText = !/^\s+$/.test(text) &&
                                !['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'].includes(text.toLowerCase());

        if (isMeaningfulText) {
          setSelectedText(text);
          setShowTextSelection(true);
        } else {
          setShowTextSelection(false);
        }
      } else {
        setShowTextSelection(false);
      }
    };

    const handleTouchEnd = () => {
      // Handle touch devices
      setTimeout(handleSelection, 100);
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('touchend', handleTouchEnd);
    document.addEventListener('selectionchange', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('touchend', handleTouchEnd);
      document.removeEventListener('selectionchange', handleSelection);
    };
  }, []);

  const loadSessionHistory = async () => {
    try {
      const response = await fetch(`${apiBaseUrl}/chat/sessions/${sessionId}/messages`);
      if (response.ok) {
        const data = await response.json();
        setMessages(data.messages || []);
      }
    } catch (error) {
      console.error('Failed to load session history:', error);
    }
  };

  const handleSend = async (useSelectedText = false) => {
    if ((!input.trim() && !useSelectedText) || isLoading) return;

    const messageText = useSelectedText
      ? `About the selected text: ${selectedText}`
      : input.trim();

    const userMessage: ChatMessage = {
      role: 'user',
      content: messageText,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setSelectedText('');
    setShowTextSelection(false);
    setIsLoading(true);

    try {
      const payload: any = {
        message: messageText,
        session_id: sessionId || undefined
      };

      if (useSelectedText) {
        payload.selected_text = selectedText;
      }

      const response = await fetch(`${apiBaseUrl}/chat/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();

      // Update session ID if new
      if (data.session_id && data.session_id !== sessionId) {
        setSessionId(data.session_id);
        onSessionChange?.(data.session_id);
      }

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        sources: data.sources || [],
        contextUsed: data.context_used
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
    setIsTyping(e.target.value.length > 0);
  };

  const handleInputBlur = () => {
    setTimeout(() => setIsTyping(false), 100);
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const askAboutSelectedText = () => {
    if (selectedText) {
      setInput(`Explain this selected text: "${selectedText}"`);
      setShowTextSelection(false);
      inputRef.current?.focus();
    }
  };

  const clearSession = async () => {
    if (sessionId) {
      try {
        await fetch(`${apiBaseUrl}/chat/sessions/${sessionId}`, {
          method: 'DELETE'
        });
      } catch (error) {
        console.error('Failed to clear session:', error);
      }
    }

    setSessionId('');
    setMessages([]);
    onSessionChange?.('');
  };

  if (!isOpen) {
    return (
      <>
        <button
          className={`${styles.chatButton} ${isDarkMode ? styles.dark : styles.light}`}
          onClick={() => setIsOpen(true)}
          aria-label="Open RAG chat"
        >
          <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
          </svg>
          <span>Ask AI</span>
        </button>

        {/* Text selection popup */}
        {showTextSelection && (
          <div className={`${styles.textSelectionPopup} ${isDarkMode ? styles.dark : styles.light}`}>
            <p>📝 Text selected!</p>
            <div className={styles.selectedTextPreview}>
              "{selectedText.substring(0, 150)}{selectedText.length > 150 ? '...' : ''}"
            </div>
            <div className={styles.popupButtons}>
              <button onClick={() => handleSend(true)} className={styles.primaryButton}>
                💬 Ask about this
              </button>
              <button onClick={() => setShowTextSelection(false)} className={styles.secondaryButton}>
                ❌ Dismiss
              </button>
            </div>
          </div>
        )}
      </>
    );
  }

  return (
    <div className={`${styles.chatWindow} ${isMinimized ? styles.minimized : ''} ${isDarkMode ? styles.dark : styles.light}`}>
      <div className={`${styles.chatHeader} ${isDarkMode ? styles.dark : styles.light}`}>
        <div className={styles.headerLeft}>
          <div className={styles.statusIndicator} />
          <span>AI Chatbot</span>
          {sessionId && (
            <span className={styles.sessionIndicator}>
              Session: {sessionId.substring(0, 8)}...
            </span>
          )}
        </div>
        <div className={styles.headerRight}>
          <button
            className={styles.minimizeButton}
            onClick={() => setIsMinimized(!isMinimized)}
            aria-label={isMinimized ? "Maximize" : "Minimize"}
          >
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
              {isMinimized ? (
                <path d="M3 17v2h6v-2H3zM3 5v2h10V5H3zm10 16v-2h8v-2h-8v-2h-2v6h2zM7 9v2H3v2h4v2h2V9H7zm14 4v-2H11v2h10zm-6-4h2V7h4V5h-4V3h-2v6z"/>
              ) : (
                <path d="M19 13H5v-2h14v2z"/>
              )}
            </svg>
          </button>
          <button
            className={styles.clearButton}
            onClick={clearSession}
            aria-label="Clear session"
          >
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
            </svg>
          </button>
          <button
            className={styles.closeButton}
            onClick={() => setIsOpen(false)}
            aria-label="Close chat"
          >
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
            </svg>
          </button>
        </div>
      </div>

      {!isMinimized && (
        <>
          <div className={`${styles.messagesContainer} ${isDarkMode ? styles.dark : styles.light}`}>
            {messages.length === 0 && (
              <div className={`${styles.welcomeMessage} ${isDarkMode ? styles.dark : styles.light}`}>
                🤖 Welcome! I'm your RAG-powered robotics assistant.
                <br />
                Ask me anything about the Physical AI & Humanoid Robotics textbook!
                <br />
                <small>💡 Tip: Select any text in the book and ask questions about it!</small>
              </div>
            )}

            {messages.map((message, index) => (
              <div key={index} className={`${styles.message} ${styles[message.role]}`}>
                <div className={`${styles.messageContent} ${isDarkMode ? styles.dark : styles.light}`}>
                  {message.content}

                  {message.sources && message.sources.length > 0 && (
                    <div className={`${styles.sources} ${isDarkMode ? styles.dark : styles.light}`}>
                      <span className={styles.contextIndicator}>
                        📚 Context from textbook
                      </span>
                      <div className={styles.sourcesList}>
                        {message.sources.slice(0, 3).map((source, i) => (
                          <div key={i} className={`${styles.source} ${isDarkMode ? styles.dark : styles.light}`}>
                            {source.section && (
                              <span className={styles.sourceSection}>
                                {source.section}
                              </span>
                            )}
                            {source.file_path && (
                              <span className={styles.sourceFile}>
                                {source.file_path}
                              </span>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
                <div className={`${styles.messageTime} ${isDarkMode ? styles.dark : styles.light}`}>
                  {formatTime(message.timestamp)}
                  {message.contextUsed !== undefined && (
                    <span className={styles.contextBadge}>
                      {message.contextUsed ? '🔍' : '💭'}
                    </span>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className={`${styles.message} ${styles.assistant}`}>
                <div className={`${styles.typingIndicator} ${isDarkMode ? styles.dark : styles.light}`}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Text selection indicator */}
          {showTextSelection && (
            <div className={`${styles.selectionIndicator} ${isDarkMode ? styles.dark : styles.light}`}>
              <div className={styles.selectionContent}>
                <span className={styles.selectionLabel}>📝 Selected text:</span>
                <span className={styles.selectionText}>"{selectedText.substring(0, 80)}{selectedText.length > 80 ? '...' : ''}"</span>
              </div>
              <div className={styles.selectionActions}>
                <button onClick={askAboutSelectedText} className={styles.askButton}>
                  💬 Ask about this
                </button>
                <button onClick={() => setShowTextSelection(false)} className={styles.dismissButton}>
                  ❌
                </button>
              </div>
            </div>
          )}

          <div className={`${styles.inputContainer} ${isDarkMode ? styles.dark : styles.light}`}>
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              onBlur={handleInputBlur}
              placeholder="Ask about robotics, AI, or select text from the book..."
              className={`${styles.chatInput} ${isTyping ? styles.typing : ''} ${isDarkMode ? styles.dark : styles.light}`}
              disabled={isLoading}
            />
            <button
              onClick={() => handleSend()}
              disabled={!input.trim() || isLoading}
              className={`${styles.sendButton} ${input.trim() && !isLoading ? styles.active : ''} ${isDarkMode ? styles.dark : styles.light}`}
              aria-label="Send message"
            >
              <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
              </svg>
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default RAGChatbot;