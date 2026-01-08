class AuthService {

    static getFetchOptions(method = 'GET', body = null) {
        const options = {
            method,
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (body) {
            options.body = JSON.stringify(body);
        }

        return options;
    }

    static async logout() {
        try {
            await fetch('http://localhost:5000/api/logout', {
                method: 'POST',
                credentials: 'include'
            });
        } catch (error) {
            console.error('Erreur lors de la déconnexion:', error);
        }
    }

    // Vérifie l'authentification en appelant l'endpoint protected
    static async checkAuth() {
        try {
            const response = await fetch('http://localhost:5000/api/protected', {
                method: 'GET',
                credentials: 'include'
            });
            return response.ok;
        } catch (error) {
            return false;
        }
    }
}

export default AuthService;
