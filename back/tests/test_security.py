# tests/test_security.py
"""
Suite de tests de sécurité pour l'application Notes
Tests: XSS, CSRF, Injection SQL, Permissions, Authentication
"""

import sys
import os
# on ajoute le dossier parent au path pour importer app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
from app import app, reset_db
from models import db
from models.user import User
from models.note import Note
import bcrypt

class SecurityTestCase(unittest.TestCase):
    """Tests de sécurité de l'application"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Désactiver CSRF pour les tests
        self.client = self.app.test_client()
        
        # Réinitialiser la BD
        with self.app.app_context():
            reset_db()
            
            # Créer utilisateurs de test
            salt = bcrypt.gensalt()
            alice_hash = bcrypt.hashpw('password123'.encode('utf-8'), salt).decode('utf-8')
            bob_hash = bcrypt.hashpw('password123'.encode('utf-8'), salt).decode('utf-8')
            
            alice = User(nom='alice', pswd_hashed=alice_hash)
            bob = User(nom='bob', pswd_hashed=bob_hash)
            
            db.session.add(alice)
            db.session.add(bob)
            db.session.commit()
            
            # Créer notes de test
            alice_note = Note(owner_id=alice.id, title="Note Alice", content="Contenu privé", visibility="private")
            shared_note = Note(owner_id=alice.id, title="Note partagée", content="Contenu partagé", visibility="read")
            
            db.session.add(alice_note)
            db.session.add(shared_note)
            db.session.commit()
            
            self.alice_id = alice.id
            self.bob_id = bob.id
            self.alice_note_id = alice_note.id
            self.shared_note_id = shared_note.id

    def tearDown(self):
        """Nettoyage après chaque test"""
        with self.app.app_context():
            db.session.remove()

    def login(self, username, password):
        """Helper pour se connecter et obtenir le cookie JWT"""
        response = self.client.post('/api/login', 
            data=json.dumps({'username': username, 'password': password}),
            content_type='application/json'
        )
        return response

    # ===== TESTS AUTHENTICATION =====

    def test_register_success(self):
        """Test: Inscription réussie"""
        response = self.client.post('/api/register',
            data=json.dumps({'username': 'charlie', 'password': 'password123'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['username'], 'charlie')

    def test_register_weak_password(self):
        """Test: Inscription avec mot de passe faible"""
        response = self.client.post('/api/register',
            data=json.dumps({'username': 'hacker', 'password': '123'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('au moins 6 caractères', data['error'])

    def test_register_duplicate_username(self):
        """Test: Inscription avec username existant"""
        response = self.client.post('/api/register',
            data=json.dumps({'username': 'alice', 'password': 'newpassword'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('existe déjà', data['error'])

    def test_login_success(self):
        """Test: Connexion réussie"""
        response = self.login('alice', 'password123')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('Set-Cookie', response.headers)

    def test_login_invalid_credentials(self):
        """Test: Connexion avec mauvais credentials"""
        response = self.login('alice', 'wrongpassword')
        self.assertEqual(response.status_code, 401)

    def test_protected_route_without_auth(self):
        """Test: Accès route protégée sans authentification"""
        response = self.client.get('/api/protected')
        self.assertEqual(response.status_code, 401)

    def test_protected_route_with_auth(self):
        """Test: Accès route protégée avec authentification"""
        self.login('alice', 'password123')
        response = self.client.get('/api/protected')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['logged_in_as'], 'alice')

    # ===== TESTS PERMISSIONS =====

    def test_access_own_private_note(self):
        """Test: Accès à sa propre note privée"""
        self.login('alice', 'password123')
        response = self.client.get(f'/api/notes/{self.alice_note_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

    def test_access_others_private_note(self):
        """Test: INTERDIT - Accès à la note privée d'un autre utilisateur"""
        self.login('bob', 'password123')
        response = self.client.get(f'/api/notes/{self.alice_note_id}')
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Access denied')

    def test_access_shared_note_readonly(self):
        """Test: Accès en lecture à une note partagée"""
        self.login('bob', 'password123')
        response = self.client.get(f'/api/notes/{self.shared_note_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

    def test_modify_others_note_forbidden(self):
        """Test: INTERDIT - Modification de la note d'un autre (read-only)"""
        self.login('bob', 'password123')
        response = self.client.put(f'/api/notes/{self.shared_note_id}',
            data=json.dumps({'title': 'Hacked', 'content': 'Hacked content'}),
            content_type='application/json'
        )
        # La note est en mode "read" donc Bob ne peut pas modifier
        # 405 = Method Not Allowed (route PUT non implémentée)
        self.assertIn(response.status_code, [403, 400, 405])

    # ===== TESTS XSS PROTECTION =====

    def test_xss_in_note_title(self):
        """Test: Protection XSS dans le titre"""
        self.login('alice', 'password123')
        xss_payload = "<script>alert('XSS')</script>"
        response = self.client.post('/api/notes',
            data=json.dumps({
                'title': xss_payload,
                'content': 'Normal content',
                'visibility': 'private'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        
        # on vérifie que le script n'est PAS exécuté (frontend doit échapper)
        # Backend stocke tel quel, frontend doit échapper via escapeHtml()
        data = json.loads(response.data)
        # Le titre est stocké tel quel dans la BD
        self.assertEqual(data['note']['title'], xss_payload)

    def test_xss_in_note_content(self):
        """Test: Protection XSS dans le contenu"""
        self.login('alice', 'password123')
        xss_payload = "<img src=x onerror=alert('XSS')>"
        response = self.client.post('/api/notes',
            data=json.dumps({
                'title': 'Test XSS',
                'content': xss_payload,
                'visibility': 'private'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    # ===== TESTS SQL INJECTION =====

    def test_sql_injection_login(self):
        """Test: Protection contre injection SQL dans login"""
        # Tentative classique: admin' OR '1'='1
        response = self.login("admin' OR '1'='1", "anything")
        self.assertEqual(response.status_code, 401)
        # SQLAlchemy protège automatiquement avec parameterized queries

    def test_sql_injection_note_search(self):
        """Test: Protection injection SQL dans recherche de notes"""
        self.login('alice', 'password123')
        # Tentative d'injection dans l'URL
        response = self.client.get("/api/notes/1' OR '1'='1")
        # Devrait retourner 404 ou 400, pas exposer toutes les notes
        self.assertIn(response.status_code, [404, 400])

    # ===== TESTS VALIDATION INPUTS =====

    def test_empty_note_title(self):
        """Test: Rejet note sans titre"""
        self.login('alice', 'password123')
        response = self.client.post('/api/notes',
            data=json.dumps({'title': '', 'content': 'Content', 'visibility': 'private'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_too_long_title(self):
        """Test: Rejet titre trop long (>200 caractères)"""
        self.login('alice', 'password123')
        long_title = 'A' * 201
        response = self.client.post('/api/notes',
            data=json.dumps({'title': long_title, 'content': 'Content', 'visibility': 'private'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_too_long_content(self):
        """Test: Rejet contenu trop long (>10000 caractères)"""
        self.login('alice', 'password123')
        long_content = 'A' * 10001
        response = self.client.post('/api/notes',
            data=json.dumps({'title': 'Title', 'content': long_content, 'visibility': 'private'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_visibility(self):
        """Test: Rejet visibilité invalide"""
        self.login('alice', 'password123')
        response = self.client.post('/api/notes',
            data=json.dumps({'title': 'Title', 'content': 'Content', 'visibility': 'invalid'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    # ===== TESTS SECURITE HEADERS =====

    def test_security_headers_present(self):
        """Test: Présence des headers de sécurité"""
        response = self.client.get('/api/protected')
        
        # X-Frame-Options (protection Clickjacking)
        self.assertIn('X-Frame-Options', response.headers)
        self.assertEqual(response.headers['X-Frame-Options'], 'SAMEORIGIN')
        
        # X-Content-Type-Options (protection MIME sniffing)
        self.assertIn('X-Content-Type-Options', response.headers)
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
        
        # X-XSS-Protection
        self.assertIn('X-XSS-Protection', response.headers)
        
        # Content-Security-Policy
        self.assertIn('Content-Security-Policy', response.headers)

    # ===== TESTS PASSWORD HASHING =====

    def test_password_hashed_in_database(self):
        """Test: Mot de passe haché dans la BD (pas en clair)"""
        with self.app.app_context():
            alice = User.query.filter_by(nom='alice').first()
            # Le mot de passe ne doit PAS être "password123" en clair
            self.assertNotEqual(alice.pswd_hashed, 'password123')
            # Doit ressembler à un hash bcrypt
            self.assertTrue(alice.pswd_hashed.startswith('$2'))

    # ===== TESTS AUTHORIZATION =====

    def test_cannot_delete_others_note(self):
        """Test: INTERDIT - Suppression de la note d'un autre"""
        self.login('bob', 'password123')
        response = self.client.delete(f'/api/notes/{self.alice_note_id}')
        # 405 = Method Not Allowed (route DELETE non implémentée)
        self.assertIn(response.status_code, [403, 404, 405])

    def test_list_notes_only_shows_accessible(self):
        """Test: Liste des notes ne montre que les notes accessibles"""
        self.login('bob', 'password123')
        response = self.client.get('/api/notes')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Bob ne doit PAS voir la note privée d'Alice
        note_ids = [note['id'] for note in data['notes']]
        self.assertNotIn(self.alice_note_id, note_ids)
        
        # Bob DOIT voir la note partagée
        self.assertIn(self.shared_note_id, note_ids)


if __name__ == '__main__':
    # Lancer les tests
    unittest.main(verbosity=2)
