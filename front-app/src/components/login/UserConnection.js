import './UserConnection.css';
import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import AuthService from '../../utils/authService';

export default function UserConnection({ onUserInfoFetched }) {
    const [amIConnected, setAmIConnected] = useState(null);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const response = await fetch("http://localhost:5000/api/protected", {
                    method: "GET",
                    credentials: 'include'  // Important: sends cookies automatically
                });

                if (!response.ok) {
                    setAmIConnected(false);
                    onUserInfoFetched?.(null);
                    return;
                }

                const data = await response.json();
                setAmIConnected(true);
                onUserInfoFetched?.({ id: data.user_id, username: data.logged_in_as });
            } catch (error) {
                console.error('Error verifying authentication:', error);
                setAmIConnected(false);
                onUserInfoFetched?.(null);
            }
        };

        checkAuth();
    }, [onUserInfoFetched]);

    if (amIConnected === null) {
        return null;
    }

    const handleLogout = () => {
        fetch("http://localhost:5000/api/logout", {
            method: "POST",
            credentials: "include",
        })
            .then(response => {
                if (response.ok) {
                    setAmIConnected(false);
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error("Error during logout:", error);
            });
    };




    return (
        amIConnected ? (
            <div className="user-connection-container">
                <button className="user-connection-link red" onClick={handleLogout}>Logout</button>
            </div>
        ) : (
            <div className="user-connection-container">
                <Link to="/login" className="user-connection-link">Login</Link>
                <Link to="/register" className="user-connection-link">Register</Link>
            </div>
        )
    );
}