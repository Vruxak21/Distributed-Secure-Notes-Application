import React, { useState, useEffect } from 'react';
import './NoteDetail.css';

const NoteDetail = ({ noteId, userId, onBack }) => {
    const [note, setNote] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (noteId) {
            fetchNoteDetail();
        }
    }, [noteId]);

    const fetchNoteDetail = async () => {
        try {
            setLoading(true);
            const response = await fetch(`http://localhost:5000/api/notes/${noteId}?user_id=${userId}`);
            const data = await response.json();

            if (data.success) {
                setNote(data.note);
                setError(null);
            } else {
                setError(data.error);
            }
        } catch (err) {
            setError('Erreur de connexion au serveur');
            console.error('Error fetching note detail:', err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <div className="note-detail-loading">Chargement de la note...</div>;
    }

    if (error) {
        return (
            <div className="note-detail-error">
                <p>Erreur : {error}</p>
                <button onClick={onBack}>Retour à la liste</button>
            </div>
        );
    }

    if (!note) {
        return null;
    }

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('fr-FR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <div className="note-detail-container">
            <div className="note-detail-header">
                <button className="back-btn" onClick={onBack}>
                    ← Retour
                </button>
                <div className="note-detail-actions">
                    {note.lock && note.lock.is_locked && (
                        <span className="lock-indicator">
                            Verrouillée
                            {note.lock.locked_by_user_id === userId && " (par vous)"}
                        </span>
                    )}
                </div>
            </div>

            <div className="note-detail-content">
                <div className="note-detail-meta">
                    <div className="note-status-badges">
                        {note.is_owner ? (
                            <span className="badge badge-owner">Propriétaire</span>
                        ) : (
                            <span className={`badge badge-${note.access_level}`}>
                                {note.access_level === 'read' ? 'Lecture seule' : 'Lecture/Écriture'}
                            </span>
                        )}
                    </div>

                    <div className="note-info">
                        <p><strong>Propriétaire :</strong> {note.owner_name}</p>
                        <p><strong>Créée le :</strong> {formatDate(note.created_at)}</p>
                        <p><strong>Modifiée le :</strong> {formatDate(note.updated_at)}</p>
                    </div>
                </div>

                <div className="note-title-section">
                    <h1>{note.title}</h1>
                </div>

                <div className="note-content-section">
                    <div className="note-content-display">
                        {note.content.split('\n').map((paragraph, index) => (
                            <p key={index}>{paragraph || '\u00A0'}</p>
                        ))}
                    </div>
                </div>

                {!note.is_owner && note.access_level === 'read' && (
                    <div className="read-only-notice">
                        Lecture seule pas possible de modifier! 
                    </div>
                )}
            </div>
        </div>
    );
};

export default NoteDetail;
