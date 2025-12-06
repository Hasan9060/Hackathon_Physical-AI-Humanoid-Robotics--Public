import React, { useState, useRef, useEffect } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './ChatbotWidget.module.css';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    sources?: any[];
}

const ChatbotWidget: React.FC = () => {
    const { siteConfig } = useDocusaurusContext();
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [selectedText, setSelectedText] = useState('');
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const API_URL = (siteConfig.customFields?.apiUrl as string) || 'http://localhost:8000';

    // Scroll to bottom when messages change
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Detect text selection
    useEffect(() => {
        const handleSelection = () => {
            const selection = window.getSelection();
            const text = selection?.toString().trim();
            if (text && text.length > 10) {
                setSelectedText(text);
            }
        };

        document.addEventListener('mouseup', handleSelection);
        return () => document.removeEventListener('mouseup', handleSelection);
    }, []);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage: Message = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            console.log('Sending request to:', `${API_URL}/query`);
            console.log('Request body:', { question: input, selected_text: selectedText || null, max_results: 5 });

            const token = localStorage.getItem('token');
            const headers: HeadersInit = { 'Content-Type': 'application/json' };
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            const response = await fetch(`${API_URL}/query`, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify({
                    question: input,
                    selected_text: selectedText || null,
                    max_results: 5
                })
            });

            console.log('Response status:', response.status);
            console.log('Response ok:', response.ok);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Error response:', errorText);
                throw new Error(`Failed to get response: ${response.status} - ${errorText}`);
            }

            const data = await response.json();
            console.log('Response data:', data);

            const assistantMessage: Message = {
                role: 'assistant',
                content: data.answer,
                sources: data.sources
            };

            setMessages(prev => [...prev, assistantMessage]);
            setSelectedText(''); // Clear selected text after use
        } catch (error) {
            console.error('Detailed error:', error);
            console.error('Error message:', error instanceof Error ? error.message : 'Unknown error');
            const errorMessage: Message = {
                role: 'assistant',
                content: 'Sorry, I encountered an error. Please try again.'
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <>
            {/* Floating Chat Button */}
            <button
                className={styles.chatButton}
                onClick={() => setIsOpen(!isOpen)}
                aria-label="Open chatbot"
            >
                {isOpen ? '✕' : '💬'}
            </button>

            {/* Chat Window */}
            {isOpen && (
                <div className={styles.chatWindow}>
                    <div className={styles.chatHeader}>
                        <div className={styles.headerIcon}>🤖</div>
                        <div className={styles.headerTitle}>
                            <h3>Robotics AI</h3>
                            <p>Ask me anything!</p>
                        </div>
                    </div>

                    <div className={styles.chatMessages}>
                        {messages.length === 0 && (
                            <div className={styles.welcomeMessage}>
                                <span className={styles.welcomeIcon}>🤖</span>
                                <h3>Hello! I'm your AI Assistant.</h3>
                                <p>I can help you understand the textbook material, explain concepts, or find specific topics.</p>
                            </div>
                        )}

                        {messages.map((msg, idx) => (
                            <div
                                key={idx}
                                className={`${styles.message} ${styles[msg.role]}`}
                            >
                                {msg.role === 'assistant' ? (
                                    <div className={styles.botAvatar}>🤖</div>
                                ) : (
                                    <div className={styles.userAvatar}>👤</div>
                                )}

                                <div className={styles.messageContent}>
                                    {msg.content}

                                    {msg.sources && msg.sources.length > 0 && (
                                        <div className={styles.sources}>
                                            <details>
                                                <summary>📚 Referenced Sources</summary>
                                                {msg.sources.map((source, i) => (
                                                    <div key={i} className={styles.sourceItem}>
                                                        <strong>Source {i + 1}</strong>
                                                        <p>{source.text.substring(0, 150)}...</p>
                                                    </div>
                                                ))}
                                            </details>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}

                        {isLoading && (
                            <div className={`${styles.message} ${styles.assistant}`}>
                                <div className={styles.botAvatar}>🤖</div>
                                <div className={styles.messageContent}>
                                    <div className={styles.typingIndicator}>
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                    </div>
                                </div>
                            </div>
                        )}

                        <div ref={messagesEndRef} />
                    </div>

                    {selectedText && (
                        <div className={styles.selectedTextBanner}>
                            <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                📝 Context: "{selectedText}"
                            </span>
                            <button onClick={() => setSelectedText('')}>✕</button>
                        </div>
                    )}

                    <div className={styles.chatInput}>
                        <textarea
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Type your question here..."
                            rows={1}
                        />
                        <button
                            onClick={sendMessage}
                            disabled={!input.trim() || isLoading}
                            className={styles.sendButton}
                        >
                            ➤
                        </button>
                    </div>
                </div>
            )}
        </>
    );
};

export default ChatbotWidget;
