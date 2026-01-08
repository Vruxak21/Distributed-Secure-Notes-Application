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
            setError("Veuillez remplir tous les champs");
            setLoading(false);
            return;
        }

        try {
            const response = await fetch("http://localhost:5000/api/login", {
                method: "POST",
                credentials: 'include',  // Important: pour recevoir les cookies
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                // Le cookie JWT est automatiquement stocké par le navigateur
                window.location.href = "/";
            } else {
                setError(data.error || "Échec de la connexion");
            }
        } catch (error) {
            console.error("Erreur lors de la connexion:", error);
            setError("Erreur de connexion au serveur");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="register-container">
            <div className="register-header">
                <h2>Connexion</h2>
            </div>
            <form className="register-form" onSubmit={handleLogin}>
                {error && <div className="error-message">{error}</div>}
                <label>
                    Nom d'utilisateur :
                    <input type="text" name="username" disabled={loading} />
                </label>
                <label>
                    Mot de passe :
                    <input type="password" name="password" disabled={loading} />
                </label>
                <button type="submit" disabled={loading}>
                    {loading ? 'Connexion...' : 'Se connecter'}
                </button>
            </form>
        </div>
    );
}