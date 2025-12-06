import React, { useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from '../css/auth.module.css';
import { useHistory } from '@docusaurus/router';

export default function SignUp() {
    const { siteConfig } = useDocusaurusContext();
    const history = useHistory();
    const [step, setStep] = useState(1);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const [formData, setFormData] = useState({
        email: '',
        password: '',
        name: '',
        software_background: '',
        hardware_background: '',
        learning_goals: ''
    });

    const API_URL = (siteConfig.customFields?.apiUrl as string) || 'http://localhost:8000';

    const handleInputChange = (e) => {
        console.log(`Input change: ${e.target.name} = ${e.target.value}`);
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleOptionSelect = (field, value) => {
        console.log(`Option select: ${field} = ${value}`);
        setFormData({ ...formData, [field]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        // Transform the data to match backend expectations
        const submitData = {
            ...formData,
            // Ensure we don't send full_name if it exists
            full_name: undefined
        };

        console.log('Form data being submitted:', submitData);
        console.log('API URL:', API_URL);

        try {
            const response = await fetch(`${API_URL}/signup`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(submitData)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Signup failed');
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

    const nextStep = () => setStep(step + 1);
    const prevStep = () => setStep(step - 1);

    return (
        <Layout title="Sign Up" description="Create your personalized learning account">
            <div className={styles.authContainer}>
                <div className={styles.authCard}>
                    <h1 className={styles.title}>
                        {step === 1 ? 'Create Account' : step === 2 ? 'Your Background' : 'Learning Goals'}
                    </h1>
                    <p className={styles.subtitle}>
                        {step === 1 ? 'Join the Physical AI Lab' : step === 2 ? 'Help us personalize your content' : 'What do you want to achieve?'}
                    </p>

                    {/* Step Indicators */}
                    <div className={styles.stepIndicator}>
                        {[1, 2, 3].map(i => (
                            <div key={i} className={`${styles.stepDot} ${step >= i ? styles.active : ''}`} />
                        ))}
                    </div>

                    {error && <div className="alert alert--danger margin-bottom--md">{error}</div>}

                    <form onSubmit={handleSubmit}>
                        {step === 1 && (
                            <>
                                <div className={styles.formGroup}>
                                    <label className={styles.label}>Full Name</label>
                                    <input
                                        type="text"
                                        name="name"
                                        className={styles.input}
                                        value={formData.name}
                                        onChange={handleInputChange}
                                        required
                                        placeholder="John Doe"
                                    />
                                </div>
                                <div className={styles.formGroup}>
                                    <label className={styles.label}>Email</label>
                                    <input
                                        type="email"
                                        name="email"
                                        className={styles.input}
                                        value={formData.email}
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
                                        minLength={8}
                                    />
                                </div>
                                <button type="button" className={styles.button} onClick={nextStep}>
                                    Next: Personalization →
                                </button>
                            </>
                        )}

                        {step === 2 && (
                            <>
                                <div className={styles.formGroup}>
                                    <label className={styles.label}>Software Experience</label>
                                    {[
                                        { val: 'Beginner', icon: '👶', title: 'Beginner', desc: 'New to coding' },
                                        { val: 'Intermediate', icon: '💻', title: 'Intermediate', desc: 'Comfortable with Python/C++' },
                                        { val: 'Expert', icon: '🚀', title: 'Expert', desc: 'Professional Software Engineer' }
                                    ].map(opt => (
                                        <div
                                            key={opt.val}
                                            className={`${styles.optionCard} ${formData.software_background === opt.val ? styles.selected : ''}`}
                                            onClick={() => handleOptionSelect('software_background', opt.val)}
                                        >
                                            <span className={styles.optionIcon}>{opt.icon}</span>
                                            <div className={styles.optionContent}>
                                                <h4>{opt.title}</h4>
                                                <p>{opt.desc}</p>
                                            </div>
                                        </div>
                                    ))}
                                </div>

                                <div className={styles.formGroup}>
                                    <label className={styles.label}>Hardware Experience</label>
                                    {[
                                        { val: 'None', icon: '🚫', title: 'None', desc: 'No hardware experience' },
                                        { val: 'Hobbyist', icon: '🛠️', title: 'Hobbyist', desc: 'Arduino/Raspberry Pi projects' },
                                        { val: 'Engineer', icon: '⚡', title: 'Engineer', desc: 'Electrical/Mechanical Engineer' }
                                    ].map(opt => (
                                        <div
                                            key={opt.val}
                                            className={`${styles.optionCard} ${formData.hardware_background === opt.val ? styles.selected : ''}`}
                                            onClick={() => handleOptionSelect('hardware_background', opt.val)}
                                        >
                                            <span className={styles.optionIcon}>{opt.icon}</span>
                                            <div className={styles.optionContent}>
                                                <h4>{opt.title}</h4>
                                                <p>{opt.desc}</p>
                                            </div>
                                        </div>
                                    ))}
                                </div>

                                <div style={{ display: 'flex', gap: '1rem' }}>
                                    <button type="button" className={`${styles.button} button--secondary`} onClick={prevStep} style={{ background: 'transparent', border: '1px solid currentColor', color: 'inherit' }}>
                                        Back
                                    </button>
                                    <button type="button" className={styles.button} onClick={nextStep} disabled={!formData.software_background || !formData.hardware_background}>
                                        Next: Goals →
                                    </button>
                                </div>
                            </>
                        )}

                        {step === 3 && (
                            <>
                                <div className={styles.formGroup}>
                                    <label className={styles.label}>What are your learning goals?</label>
                                    <textarea
                                        name="learning_goals"
                                        className={styles.textarea}
                                        value={formData.learning_goals}
                                        onChange={handleInputChange}
                                        rows={4}
                                        placeholder="I want to build a walking robot..."
                                    />
                                </div>

                                <div style={{ display: 'flex', gap: '1rem' }}>
                                    <button type="button" className={`${styles.button} button--secondary`} onClick={prevStep} style={{ background: 'transparent', border: '1px solid currentColor', color: 'inherit' }}>
                                        Back
                                    </button>
                                    <button type="submit" className={styles.button} disabled={isLoading}>
                                        {isLoading ? 'Creating Account...' : 'Complete Signup ✨'}
                                    </button>
                                </div>
                            </>
                        )}

                        <p className={styles.linkText}>
                            Already have an account? <Link to="/signin" className={styles.link}>Sign In</Link>
                        </p>
                    </form>
                </div>
            </div>
        </Layout>
    );
}
