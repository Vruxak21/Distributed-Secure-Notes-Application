import React, { useCallback, useState } from 'react';
import './Home.css';
import NotesList from '../../components/notes/list/NotesList';
import NoteDetail from '../../components/notes/detail/NoteDetail';
import { NewNoteButton } from '../../components/notes/button/NewNoteButton';
import UserConnection from '../../components/login/UserConnection';

export function Home() {
    const [selectedNoteId, setSelectedNoteId] = useState(null);
    const [userInfo, setUserInfo] = useState(null);

    const isConnected = !!userInfo;

    const handleUserInfoFetched = useCallback((info) => {
        if (info) {
            setUserInfo(info);
        } else {
            setUserInfo(null);
            setSelectedNoteId(null);
        }
    }, []);

    const handleSelectNote = (noteId) => setSelectedNoteId(noteId);
    const handleBackToList = () => setSelectedNoteId(null);

    return (
        <div className="App">
            <header className="App-header">
                <h1>Notes Sécurisées</h1>
                <p className="user-info">
                    utilisateur: {userInfo?.username ?? "—"}
                </p>
            </header>


            <div><UserConnection onUserInfoFetched={handleUserInfoFetched}/>
            </div>


            <main className="App-main">

                {isConnected ? (

                    <NewNoteButton userInfo={userInfo} />,
                    selectedNoteId ? (
                        <NoteDetail
                            noteId={selectedNoteId}
                            userId={userInfo.id}
                            onBack={handleBackToList}
                        />
                    ) : (
                        <NotesList
                            userId={userInfo.id}
                            onSelectNote={handleSelectNote}
                        />
                    )
                ) : (
                    <div>Connecte-toi pour voir tes notes.</div>
                )}
            </main>
        </div>
    );
}