import React, { useState } from 'react';
import './Home.css';
import NotesList from '../../components/NotesList';
import NoteDetail from '../../components/NoteDetail';
import UserConnection from '../../components/login/UserConnection';

export function Home() {
    // TODO: Matthieu remplacer par l'authentification
    const [userId, setUserId] = useState(null); // ID user temp 
    const [username, setUsername] = useState(null)
    const [selectedNoteId, setSelectedNoteId] = useState(null);
    const handleUserInfoFetched = (userInfo) => {
        setUserId(userInfo.id);
        setUsername(userInfo.username);
        
    };
    

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
                <p className="user-info">
                    utilisateur: {username} #{userId}</p>
            </header>

            <div><UserConnection onUserInfoFetched={handleUserInfoFetched}/></div>

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