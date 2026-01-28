import './Register.css';
import AuthService from '../../utils/authService';
import { useState } from 'react';

export function Register() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleRegister = async (e) => {
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

        if (password.length < 6) {
            setError("Password must contain at least 6 characters");
            setLoading(false);
            return;
        }

        try {
            const response = await fetch("http://localhost:5000/api/register", {
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
                setError(data.error || "Registration failed");
            }
        } catch (error) {
            console.error("Error during registration:", error);
            setError("Server connection error");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="register-container">
            <div className="register-header">
                <h2>Register</h2>
            </div>
            <form className="register-form" onSubmit={handleRegister}>
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
                    {loading ? 'Registering...' : 'Sign Up'}
                </button>
            </form>
        </div>
    );
}