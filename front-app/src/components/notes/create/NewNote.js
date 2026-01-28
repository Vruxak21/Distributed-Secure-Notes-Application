import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './NewNote.css';

export function NewNote() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [visibility, setVisibility] = useState('private');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const resp = await fetch('http://localhost:5000/api/notes', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content, visibility }),
      });
      const data = await resp.json();
      if (!resp.ok) {
        setError(data.error || 'Error during creation');
      } else {
        navigate('/');
      }
    } catch (err) {
      setError('Server connection error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="new-note-page">
      <div className="new-note-card">
        <h2>Create a new note</h2>
        <form onSubmit={handleSubmit} className="new-note-form">
          <label>
            Title
            <input value={title} onChange={(e) => setTitle(e.target.value)} required />
          </label>
          <label>
            Content
            <textarea value={content} onChange={(e) => setContent(e.target.value)} required rows={6} />
          </label>
          <label>
            Visibility
            <select value={visibility} onChange={(e) => setVisibility(e.target.value)}>
              <option value="private">Private</option>
              <option value="read">Read Only</option>
              <option value="write">Read/Write</option>
            </select>
          </label>
          {error && <div className="form-error">{error}</div>}
          <div className="form-actions">
            <button type="button" className="ghost" onClick={() => navigate('/')}>Cancel</button>
            <button type="submit" disabled={loading}>
              {loading ? 'Creating...' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}