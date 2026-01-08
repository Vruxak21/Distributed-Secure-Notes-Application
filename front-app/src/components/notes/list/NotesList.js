import React, { useState, useEffect } from 'react';
import './NotesList.css';
import { NewNoteButton } from '../button/NewNoteButton';
import AuthService from '../../../utils/authService';

const NotesList = ({ userId, onSelectNote }) => {
    const [notes, setNotes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filter, setFilter] = useState('all');

    useEffect(() => {
        fetchNotes();
    }, [userId]);

    const fetchNotes = async () => {
        try {
            setLoading(true);
            const response = await fetch('http://localhost:5000/api/notes', {
                method: 'GET',
                credentials: 'include'  // Important: envoie les cookies automatiquement
            });

            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }

            const data = await response.json();

            if (data.success) {
                setNotes(data.notes);
                setError(null);
            } else {
                setError(data.error);
            }
        } catch (err) {
            setError('Erreur de connexion au serveur');
            console.error('Error fetching notes:', err);
        } finally {
            setLoading(false);
        }
    };

    const filteredNotes = notes.filter(note => {
        if (filter === 'owned') return note.is_owner;
        if (filter === 'shared') return !note.is_owner;
        return true;
    });

    const getAccessBadge = (note) => {
        if (note.is_owner) {
            return <span className="badge badge-owner">Propriétaire</span>;
        }
        return (
            <span className={`badge badge-${note.visibility}`}>
                {note.visibility === 'read' ? 'Lecture seule' : 'Lecture/Écriture '}
            </span>
        );
    };

    if (loading) {
        return <div className="notes-loading">Chargement des notes...</div>;
    }

    if (error) {
        return (
            <div className="notes-error">
                <p>Erreur : {error}</p>
                <button onClick={fetchNotes}>Réessayer</button>
            </div>
        );
    }

    return (
        <div className="notes-list-container">
            <div className="notes-header">
                <h2>Mes Notes</h2>
                <div className="notes-actions">
                    <NewNoteButton userId={userId} />
                    <button className="refresh-btn" onClick={fetchNotes}>Actualiser</button>
                </div>

            </div>

            <div className="filter-buttons">
                <button
                    className={filter === 'all' ? 'active' : ''}
                    onClick={() => setFilter('all')}
                >
                    Toutes ({notes.length})
                </button>
                <button
                    className={filter === 'owned' ? 'active' : ''}
                    onClick={() => setFilter('owned')}
                >
                    Mes notes ({notes.filter(n => n.is_owner).length})
                </button>
                <button
                    className={filter === 'shared' ? 'active' : ''}
                    onClick={() => setFilter('shared')}
                >
                    Partagées ({notes.filter(n => !n.is_owner).length})
                </button>
            </div>

            {filteredNotes.length === 0 ? (
                <div className="no-notes">
                    <p>Aucune note à afficher</p>
                </div>
            ) : (
                <div className="notes-grid">
                    {filteredNotes.map(note => (
                        <div
                            key={note.id}
                            className="note-card"
                            onClick={() => onSelectNote(note.id)}
                        >
                            <div className="note-card-header">
                                <h3>{note.title}</h3>
                                {getAccessBadge(note)}
                            </div>
                            <div className="note-card-content">
                                <p>{note.content.substring(0, 100)}...</p>
                            </div>
                            <div className="note-card-footer">
                                <span className="note-owner">{note.owner_name}</span>
                                <span className="note-date">
                                    {new Date(note.updated_at).toLocaleDateString('fr-FR')}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default NotesList;
