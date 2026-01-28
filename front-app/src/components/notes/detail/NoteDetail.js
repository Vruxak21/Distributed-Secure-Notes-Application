import React, { useState, useEffect } from 'react';
import './NoteDetail.css';
import { escapeHtml } from '../../../utils/security';
import { Link, useNavigate } from 'react-router-dom';

const NoteDetail = ({ noteId, userId, onBack }) => {
    const [note, setNote] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (noteId) {
            fetchNoteDetail();
        }
    }, [noteId]);

    const fetchNoteDetail = async () => {
        try {
            setLoading(true);
            const response = await fetch(`http://localhost:5000/api/notes/${noteId}`, {
                method: 'GET',
                credentials: 'include'  // Important: sends cookies automatically
            });

            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }

            const data = await response.json();

            if (data.success) {
                setNote(data.note);
                console.log(data.note, userId);
                if (data.note.lock.locked && data.note.lock.user_id == userId) {
                    navigate(`/notes/${noteId}/edit/`);
                }
                setError(null);
            } else {
                setError(data.error);
            }
        } catch (err) {
            setError('Server connection error');
            console.error('Error fetching note detail:', err);
        } finally {
            setLoading(false);
        }
    }

    if (loading) {
        return <div className="note-detail-loading">Loading note...</div>;
    }

    if (error) {
        return (
            <div className="note-detail-error">
                <p>Error: {error}</p>
                <button onClick={onBack}>Back to list</button>
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
                    Back
                </button>
                <div className="note-detail-actions">
                    {note.lock && note.lock.is_locked && (
                        <span className="lock-indicator">
                            Locked
                            {note.lock.locked_by_user_id === userId && " (by you)"}
                        </span>
                    )}
                </div>
            </div>

            <div className="note-detail-content">
                <div className="note-detail-meta">
                    <div className="note-status-badges">
                        {note.is_owner ? (
                            <span className="badge badge-owner">Owner</span>
                        ) : (
                            <span className={`badge badge-${note.access_level}`}>
                                {note.access_level === 'read' ? 'Read Only' : 'Read/Write'}
                            </span>
                        )}
                    </div>

                    <div className="note-info">
                        <p><strong>Owner:</strong> {note.owner_name}</p>
                        <p><strong>Created on:</strong> {formatDate(note.created_at)}</p>
                        <p><strong>Modified on:</strong> {formatDate(note.updated_at)}</p>
                    </div>
                </div>

                <div className="note-title-section">
                    <h1>{note.title}</h1>
                </div>

                <div className="note-content-section">
                    <div className="note-content-display">
                        {note.content.split('\n').map((paragraph, index) => (
                            <p key={index} dangerouslySetInnerHTML={{ __html: escapeHtml(paragraph) || '\u00A0' }} />
                        ))}
                    </div>
                </div>

                {!note.is_owner && note.access_level === 'read' && (
                    <div className="read-only-notice">
                        Read only - cannot modify!
                    </div>
                )}

                {(note.is_owner || note.access_level === 'write') && note.lock.locked == false && (
                    <div className="note-edit-section">
                        <Link className="edit-note-btn" to={`/notes/${noteId}/edit/`}>
                            Edit note
                        </Link>
                    </div>
                )}

                {(note.access_level === 'write' && note.lock.locked) && (
                    <div className="read-only-notice">
                        This note is currently locked by another user. You cannot edit it at the moment.
                    </div>
                )}

            </div>
        </div >
    );
};

export default NoteDetail;
