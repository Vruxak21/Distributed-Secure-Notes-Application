import '../Register/Register.css';
import AuthService from '../../utils/authService';
import { useState } from 'react';

export function Login() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        const username = document.querySelector('input[name="username"]').value.trim();
        const password = document.querySelector('input[name="password"]').value;

        if (!username || !password) {
            setError("Please fill in all fields");
            setLoading(false);
            return;
        }

        try {
            const response = await fetch("http://localhost:5000/api/login", {
                method: "POST",
                credentials: 'include',  // Important: to receive cookies
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                // JWT cookie is automatically stored by the browser
                window.location.href = "/";
            } else {
                setError(data.error || "Login failed");
            }
        } catch (error) {
            console.error("Error during login:", error);
            setError("Server connection error");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="register-container">
            <div className="register-header">
                <h2>Login</h2>
            </div>
            <form className="register-form" onSubmit={handleLogin}>
                {error && <div className="error-message">{error}</div>}
                <label>
                    Username:
                    <input type="text" name="username" disabled={loading} />
                </label>
                <label>
                    Password:
                    <input type="password" name="password" disabled={loading} />
                </label>
                <button type="submit" disabled={loading}>
                    {loading ? 'Logging in...' : 'Sign In'}
                </button>
            </form>
        </div>
    );
}