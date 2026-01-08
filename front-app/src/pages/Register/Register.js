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
            setError("Veuillez remplir tous les champs");
            setLoading(false);
            return;
        }

        if (password.length < 6) {
            setError("Le mot de passe doit contenir au moins 6 caractères");
            setLoading(false);
            return;
        }

        try {
            const response = await fetch("http://localhost:5000/api/register", {
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
                setError(data.error || "Échec de l'inscription");
            }
        } catch (error) {
            console.error("Erreur lors de l'inscription:", error);
            setError("Erreur de connexion au serveur");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="register-container">
            <div className="register-header">
                <h2>Inscription</h2>
            </div>
            <form className="register-form" onSubmit={handleRegister}>
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
                    {loading ? 'Inscription...' : 'S\'inscrire'}
                </button>
            </form>
        </div>
    );
}