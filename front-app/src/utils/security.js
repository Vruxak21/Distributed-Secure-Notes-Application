/**
 * Protège contre les attaques XSS en échappant les caractères HTML dangereux
 */
export function sanitizeHtml(text) {
    if (!text) return '';

    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Valide la longueur d'une entrée utilisateur
 */
export function validateInput(input, maxLength = 10000) {
    if (!input) return false;
    if (typeof input !== 'string') return false;
    if (input.length > maxLength) return false;
    return true;
}

/**
 * Échappe les caractères spéciaux pour affichage sécurisé
 */
export function escapeHtml(unsafe) {
    if (!unsafe) return '';

    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
