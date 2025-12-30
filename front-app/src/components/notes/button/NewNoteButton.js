import { useNavigate } from 'react-router-dom';
import './NewNoteButton.css';

export function NewNoteButton({ userId, className = '' }) {
  const navigate = useNavigate();
  if (!userId) return null;

  const handleClick = () => navigate('/notes/new');

  return (
    <button className={`new-note-btn ${className}`.trim()} onClick={handleClick}>
      + Nouvelle note
    </button>
  );
}