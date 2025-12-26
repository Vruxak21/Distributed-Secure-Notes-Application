from app import app, db, User, Note, Permission
from werkzeug.security import generate_password_hash

def init_test_data():
    """Initialise la base de données avec des données de test"""
    with app.app_context():
        # Créer des utilisateurs de test
        user1 = User(
            nom="Alice",
            pswd_hashe=generate_password_hash("password123")
        )
        user2 = User(
            nom="Bob",
            pswd_hashe=generate_password_hash("password456")
        )
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        # Créer des notes pour Alice (user1)
        note1 = Note(
            owner_id=user1.id,
            title="Ma première note",
            content="Ceci est le contenu de ma première note.\nElle contient plusieurs lignes.\nC'est super!"
        )
        
        note2 = Note(
            owner_id=user1.id,
            title="Liste de courses",
            content="- Pain\n- Lait\n- Œufs\n- Fromage\n- Fruits"
        )
        
        note3 = Note(
            owner_id=user1.id,
            title="Idées de projet",
            content="1. Application de notes sécurisée\n2. Gestionnaire de tâches\n3. Blog personnel\n4. Portfolio en ligne"
        )
        
        # Créer des notes pour Bob (user2)
        note4 = Note(
            owner_id=user2.id,
            title="Réunion importante",
            content="Points à aborder:\n- Budget 2024\n- Nouveaux projets\n- Recrutement\n\nDate: 15 janvier 2024"
        )
        
        note5 = Note(
            owner_id=user2.id,
            title="Notes de lecture",
            content="Livre: Sécurité des applications web\n\nPoints importants:\n- XSS\n- CSRF\n- SQL Injection\n- Authentification sécurisée"
        )
        
        db.session.add_all([note1, note2, note3, note4, note5])
        db.session.commit()
        
        # Créer des permissions de partage
        # Bob partage sa note4 en lecture seule avec Alice
        perm1 = Permission(
            note_id=note4.id,
            user_id=user1.id,
            access="read"
        )
        
        # Bob partage sa note5 en lecture/écriture avec Alice
        perm2 = Permission(
            note_id=note5.id,
            user_id=user1.id,
            access="write"
        )
        
        db.session.add_all([perm1, perm2])
        db.session.commit()
        
        # Répliquer dans la base replica
        replica_engine = db.engines['replica']
        
        # Ajouter les utilisateurs à la replica
        with replica_engine.connect() as conn:
            conn.execute(db.text(
                "INSERT INTO users (id, nom, pswd_hashe) VALUES (:id, :nom, :pswd)"
            ), [
                {"id": user1.id, "nom": user1.nom, "pswd": user1.pswd_hashe},
                {"id": user2.id, "nom": user2.nom, "pswd": user2.pswd_hashe}
            ])
            
            # Ajouter les notes à la replica
            for note in [note1, note2, note3, note4, note5]:
                conn.execute(db.text(
                    "INSERT INTO notes (id, owner_id, title, content, created_at, updated_at) "
                    "VALUES (:id, :owner_id, :title, :content, :created_at, :updated_at)"
                ), {
                    "id": note.id,
                    "owner_id": note.owner_id,
                    "title": note.title,
                    "content": note.content,
                    "created_at": note.created_at,
                    "updated_at": note.updated_at
                })
            
            # Ajouter les permissions à la replica
            conn.execute(db.text(
                "INSERT INTO permissions (note_id, user_id, access) VALUES (:note_id, :user_id, :access)"
            ), [
                {"note_id": perm1.note_id, "user_id": perm1.user_id, "access": perm1.access},
                {"note_id": perm2.note_id, "user_id": perm2.user_id, "access": perm2.access}
            ])
            
            conn.commit()
        
        print("\nDonnées de test créées avec succès!")
        print(f"\nUtilisateurs créés:")
        print(f"   - Alice (ID: {user1.id})")
        print(f"   - Bob (ID: {user2.id})")
        print(f"\nNotes créées:")
        print(f"   - {len([note1, note2, note3])} notes pour Alice")
        print(f"   - {len([note4, note5])} notes pour Bob")
        print(f"\nPartages:")
        print(f"   - Bob a partagé 'Réunion importante' en lecture seule avec Alice")
        print(f"   - Bob a partagé 'Notes de lecture' en lecture/écriture avec Alice")
        print(f"\nPour tester dans le frontend, utilisez l'ID utilisateur 1 (Alice)")

if __name__ == '__main__':
    init_test_data()
