import './UserConnection.css';
import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';

export default function UserConnection() {
    const [amIConnected, setAmIConnected] = useState(null);

    useEffect(() => {
        fetch("http://localhost:5000/api/protected", {
            method: "GET",
            credentials: "include",
        })
            .then(response => {
                setAmIConnected(response.ok);
            })
            .catch(() => {
                setAmIConnected(false);
            });
    }, []);

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