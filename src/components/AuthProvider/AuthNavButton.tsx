import React, { useState, useEffect } from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function AuthNavButton(): JSX.Element {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userProfile, setUserProfile] = useState<any>(null);

    useEffect(() => {
        // Check if user is logged in
        const token = localStorage.getItem('token');
        const profile = localStorage.getItem('user_profile');

        if (token && profile) {
            setIsLoggedIn(true);
            try {
                setUserProfile(JSON.parse(profile));
            } catch (e) {
                console.error('Failed to parse user profile:', e);
            }
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user_profile');
        setIsLoggedIn(false);
        setUserProfile(null);
        window.location.reload();
    };

    if (isLoggedIn && userProfile) {
        return (
            <div className={styles.authNavContainer}>
                <span className={styles.userName}>{userProfile.full_name || userProfile.email}</span>
                <button onClick={handleLogout} className={styles.logoutButton}>
                    Logout
                </button>
            </div>
        );
    }

    return (
        <div className={styles.authNavContainer}>
            <Link to="/signin" className={styles.signInLink}>
                Sign In
            </Link>
        </div>
    );
}
