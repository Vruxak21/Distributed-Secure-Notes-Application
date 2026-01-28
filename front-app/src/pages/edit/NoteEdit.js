import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import "./NoteEdit.css";

export default function NoteEdit() {

    const navigate = useNavigate();
    const { id: noteId } = useParams();
    const [note, setNote] = useState(null);
    const [isSaving, setIsSaving] = useState(false);
    const [message, setMessage] = useState("");

    useEffect(() => {
        const checkRights = async () => {
            const response = await fetch(`http://localhost:5000/api/notes/${noteId}/edit`, {
                method: 'GET',
                credentials: 'include'
            });
            if (response.status === 404) {
                navigate('/');
                return;
            }
            if (response.status === 403) {
                alert('You do not have permission to edit this note.');
                navigate('/');
                return;
            }

            const data = await response.json();
            if (data.success) {
                setNote(data.note);
            } else {
                navigate('/');
            }
        };
        checkRights();
    }, [navigate, noteId]);

    const saveNote = async () => {
        setIsSaving(true);
        setMessage("");
        try {
            const response = await fetch(`http://localhost:5000/api/notes/${noteId}/edit`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    title: note.title,
                    content: note.content,
                }),
            });
            if (response.ok) {
                setMessage("Note saved successfully.");
                setTimeout(() => {
                    navigate(`/`);
                }, 1200);
            } else {
                setMessage("Failed to save note.");
            }
        } catch (error) {
            setMessage("Error saving note. Try again later.");
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <div className="note-edit-outer">
            <div className="note-edit-container">
                <h1 className="note-edit-title-main">Note edit</h1>
                {note && (
                    <div className="note-edit-creator">
                        <span>Creator: <strong>{note.owner_name}</strong></span>
                    </div>
                )}
                <div className="note-edit-title">
                    <textarea
                        value={note ? note.title : ""}
                        onChange={(e) => setNote({ ...note, title: e.target.value })}
                    />
                </div>
                <div className="note-edit-content">
                    <textarea
                        value={note ? note.content : ""}
                        onChange={(e) => setNote({ ...note, content: e.target.value })}
                    />
                </div>
                {message && (
                    <div className="note-edit-message">{message}</div>
                )}
                <button className="save-note-btn" onClick={saveNote} disabled={isSaving}>
                    {isSaving ? 'Saving...' : 'Save'}
                </button>
            </div>
        </div>
    );
}