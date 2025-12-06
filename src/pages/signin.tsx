import React, { useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from '../css/auth.module.css';
import { useHistory } from '@docusaurus/router';

export default function SignIn() {
    const { siteConfig } = useDocusaurusContext();
    const history = useHistory();
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const [formData, setFormData] = useState({
        username: '', // OAuth2 form uses 'username' for email
        password: ''
    });

    const API_URL = (siteConfig.customFields?.apiUrl as string) || 'http://localhost:8000';

    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        try {
            // OAuth2 password flow requires form data
            const formBody = new URLSearchParams();
            formBody.append('username', formData.username);
            formBody.append('password', formData.password);

            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formBody
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Login failed');
            }

            // Save token
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user_profile', JSON.stringify(data.user_profile));

            // Redirect to home
            history.push('/');

            // Reload to update UI state
            window.location.reload();
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Layout title="Sign In" description="Login to your account">
            <div className={styles.authContainer}>
                <div className={styles.authCard}>
                    <h1 className={styles.title}>Welcome Back</h1>
                    <p className={styles.subtitle}>Sign in to continue learning</p>

                    {error && <div className="alert alert--danger margin-bottom--md">{error}</div>}

                    <form onSubmit={handleSubmit}>
                        <div className={styles.formGroup}>
                            <label className={styles.label}>Email</label>
                            <input
                                type="email"
                                name="username"
                                className={styles.input}
                                value={formData.username}
                                onChange={handleInputChange}
                                required
                                placeholder="john@example.com"
                            />
                        </div>
                        <div className={styles.formGroup}>
                            <label className={styles.label}>Password</label>
                            <input
                                type="password"
                                name="password"
                                className={styles.input}
                                value={formData.password}
                                onChange={handleInputChange}
                                required
                                placeholder="••••••••"
                            />
                        </div>

                        <button type="submit" className={styles.button} disabled={isLoading}>
                            {isLoading ? 'Signing In...' : 'Sign In'}
                        </button>

                        <p className={styles.linkText}>
                            Don't have an account? <Link to="/signup" className={styles.link}>Sign Up</Link>
                        </p>
                    </form>
                </div>
            </div>
        </Layout>
    );
}
