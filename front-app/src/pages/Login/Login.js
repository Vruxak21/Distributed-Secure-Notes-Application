import '../Register/Register.css';

export function Login() {
    const handleLogin = () => {
        const username = document.querySelector('input[name="username"]').value;
        const password = document.querySelector('input[name="password"]').value;

        if (username && password) {
            fetch("http://localhost:5000/api/login", {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            })
                .then(async (response) => {
                    const data = await response.json();
                    if (response.ok) {
                        window.location.href = "/";
                    } else {
                        alert("Login failed: " + data.error);
                        console.error("Error during login:", data);
                    }
                })
                .catch((error) => {
                    console.error("Error during login:", error);
                });
        } else {
            alert("Fill in all fields.");
        }
    };

    return (
        <div className="register-container">
            <div className="register-header">
                <h2>Login</h2>
            </div>
            <div className="register-form">
                <label>
                    Username :
                    <input type="text" name="username" />
                </label>
                <label>
                    Password :
                    <input type="password" name="password" />
                </label>
                <button onClick={handleLogin}>Login</button>
            </div>
        </div>
    );
}