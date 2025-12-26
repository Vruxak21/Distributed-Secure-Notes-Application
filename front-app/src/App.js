import React, { useState } from 'react';
import './App.css';
import NotesList from './components/NotesList';
import NoteDetail from './components/NoteDetail';

function App() {
  // TODO: Matthieu remplacer par l'authentification
  const [userId] = useState(1); // ID user temp 
  const [selectedNoteId, setSelectedNoteId] = useState(null);

  const handleSelectNote = (noteId) => {
    setSelectedNoteId(noteId);
  };

  const handleBackToList = () => {
    setSelectedNoteId(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Notes Sécurisées</h1>
        <p className="user-info">utilisateur: User #{userId}</p>
      </header>

      <main className="App-main">
        {selectedNoteId ? (
          <NoteDetail
            noteId={selectedNoteId}
            userId={userId}
            onBack={handleBackToList}
          />
        ) : (
          <NotesList
            userId={userId}
            onSelectNote={handleSelectNote}
          />
        )}
      </main>
    </div>
  );
}

export default App;
