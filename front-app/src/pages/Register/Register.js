import './Register.css';

export function Register() {
    const handleRegister = () => {
        const username = document.querySelector('input[name="username"]').value;
        const password = document.querySelector('input[name="password"]').value;

        if (username && password) {
            fetch("http://localhost:5000/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            })
                .then(async (response) => {
                    const data = await response.json();
                    if (response.ok) {
                        alert("Registration successful! You can now log in.");
                    } else {
                        alert("Registration failed: " + data.error);
                        console.error("Error during registration:", data);
                    }
                })
                .catch((error) => {
                    console.error("Error during registration:", error);
                });
        } else {
            alert("Fill in all fields.");
        }

    };

    return (
        <div className="register-container">
            <div className="register-header">
                <h2>Inscription</h2>
            </div>
            <div className="register-form">
                <label>
                    Nom d'utilisateur :
                    <input type="text" name="username" />
                </label>
                <label>
                    Mot de passe :
                    <input type="password" name="password" />
                </label>
                <button onClick={() => handleRegister()}>S'inscrire</button>
            </div>
        </div>
    );
}