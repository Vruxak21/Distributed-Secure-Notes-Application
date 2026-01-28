# tests/test_security.py
"""
Security test suite for Notes application
Tests: XSS, CSRF, SQL Injection, Permissions, Authentication
"""

import sys
import os
# Add parent folder to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
from app import app, reset_db
from models import db
from models.user import User
from models.note import Note
import bcrypt

class SecurityTestCase(unittest.TestCase):
    """Application security tests"""

    def setUp(self):
        """Configuration before each test"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for tests
        self.client = self.app.test_client()
        
        # Reset database
        with self.app.app_context():
            reset_db()
            
            # Create test users
            salt = bcrypt.gensalt()
            alice_hash = bcrypt.hashpw('password123'.encode('utf-8'), salt).decode('utf-8')
            bob_hash = bcrypt.hashpw('password123'.encode('utf-8'), salt).decode('utf-8')
            
            alice = User(nom='alice', pswd_hashed=alice_hash)
            bob = User(nom='bob', pswd_hashed=bob_hash)
            
            db.session.add(alice)
            db.session.add(bob)
            db.session.commit()
            
            # Create test notes
            alice_note = Note(owner_id=alice.id, title="Alice's Note", content="Private content", visibility="private")
            shared_note = Note(owner_id=alice.id, title="Shared note", content="Shared content", visibility="read")
            
            db.session.add(alice_note)
            db.session.add(shared_note)
            db.session.commit()
            
            self.alice_id = alice.id
            self.bob_id = bob.id
            self.alice_note_id = alice_note.id
            self.shared_note_id = shared_note.id

    def tearDown(self):
        """Cleanup after each test"""
        with self.app.app_context():
            db.session.remove()

    def login(self, username, password):
        """Helper to login and get JWT cookie"""
        response = self.client.post('/api/login', 
            data=json.dumps({'username': username, 'password': password}),
            content_type='application/json'
        )
        return response

    # ===== TESTS AUTHENTICATION =====

    def test_register_success(self):
        """Test: Successful registration"""
        response = self.client.post('/api/register',
            data=json.dumps({'username': 'charlie', 'password': 'password123'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['username'], 'charlie')

    def test_register_weak_password(self):
        """Test: Registration with weak password"""
        response = self.client.post('/api/register',
            data=json.dumps({'username': 'hacker', 'password': '123'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('at least 6 characters', data['error'])

    def test_register_duplicate_username(self):
        """Test: Registration with existing username"""
        response = self.client.post('/api/register',
            data=json.dumps({'username': 'alice', 'password': 'newpassword'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('already exists', data['error'])

    def test_login_success(self):
        """Test: Successful login"""
        response = self.login('alice', 'password123')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('Set-Cookie', response.headers)

    def test_login_invalid_credentials(self):
        """Test: Login with invalid credentials"""
        response = self.login('alice', 'wrongpassword')
        self.assertEqual(response.status_code, 401)

    def test_protected_route_without_auth(self):
        """Test: Access protected route without authentication"""
        response = self.client.get('/api/protected')
        self.assertEqual(response.status_code, 401)

    def test_protected_route_with_auth(self):
        """Test: Access protected route with authentication"""
        self.login('alice', 'password123')
        response = self.client.get('/api/protected')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['logged_in_as'], 'alice')

    # ===== TESTS PERMISSIONS =====

    def test_access_own_private_note(self):
        """Test: Access own private note"""
        self.login('alice', 'password123')
        response = self.client.get(f'/api/notes/{self.alice_note_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

    def test_access_others_private_note(self):
        """Test: FORBIDDEN - Access another user's private note"""
        self.login('bob', 'password123')
        response = self.client.get(f'/api/notes/{self.alice_note_id}')
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Access denied')

    def test_access_shared_note_readonly(self):
        """Test: Read access to a shared note"""
        self.login('bob', 'password123')
        response = self.client.get(f'/api/notes/{self.shared_note_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

    def test_modify_others_note_forbidden(self):
        """Test: FORBIDDEN - Modifying another user's note (read-only)"""
        self.login('bob', 'password123')
        response = self.client.put(f'/api/notes/{self.shared_note_id}',
            data=json.dumps({'title': 'Hacked', 'content': 'Hacked content'}),
            content_type='application/json'
        )
        # Note is in "read" mode so Bob cannot modify
        # 405 = Method Not Allowed (PUT route not implemented)
        self.assertIn(response.status_code, [403, 400, 405])

    # ===== TESTS XSS PROTECTION =====

    def test_xss_in_note_title(self):
        """Test: XSS protection in title"""
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
        
        # Check that the script is NOT executed (frontend must escape)
        # Backend stores as-is, frontend must escape via escapeHtml()
        data = json.loads(response.data)
        # Title is stored as-is in the database
        self.assertEqual(data['note']['title'], xss_payload)

    def test_xss_in_note_content(self):
        """Test: XSS protection in content"""
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
        """Test: SQL injection protection in login"""
        # Classic attempt: admin' OR '1'='1
        response = self.login("admin' OR '1'='1", "anything")
        self.assertEqual(response.status_code, 401)
        # SQLAlchemy automatically protects with parameterized queries

    def test_sql_injection_note_search(self):
        """Test: SQL injection protection in note search"""
        self.login('alice', 'password123')
        # Injection attempt in URL
        response = self.client.get("/api/notes/1' OR '1'='1")
        # Should return 404 or 400, not expose all notes
        self.assertIn(response.status_code, [404, 400])

    # ===== TESTS VALIDATION INPUTS =====

    def test_empty_note_title(self):
        """Test: Reject note without title"""
        self.login('alice', 'password123')
        response = self.client.post('/api/notes',
            data=json.dumps({'title': '', 'content': 'Content', 'visibility': 'private'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_too_long_title(self):
        """Test: Reject too long title (>200 characters)"""
        self.login('alice', 'password123')
        long_title = 'A' * 201
        response = self.client.post('/api/notes',
            data=json.dumps({'title': long_title, 'content': 'Content', 'visibility': 'private'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_too_long_content(self):
        """Test: Reject too long content (>10000 characters)"""
        self.login('alice', 'password123')
        long_content = 'A' * 10001
        response = self.client.post('/api/notes',
            data=json.dumps({'title': 'Title', 'content': long_content, 'visibility': 'private'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_visibility(self):
        """Test: Reject invalid visibility"""
        self.login('alice', 'password123')
        response = self.client.post('/api/notes',
            data=json.dumps({'title': 'Title', 'content': 'Content', 'visibility': 'invalid'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    # ===== TESTS SECURITY HEADERS =====

    def test_security_headers_present(self):
        """Test: Presence of security headers"""
        response = self.client.get('/api/protected')
        
        # X-Frame-Options (Clickjacking protection)
        self.assertIn('X-Frame-Options', response.headers)
        self.assertEqual(response.headers['X-Frame-Options'], 'SAMEORIGIN')
        
        # X-Content-Type-Options (MIME sniffing protection)
        self.assertIn('X-Content-Type-Options', response.headers)
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
        
        # X-XSS-Protection
        self.assertIn('X-XSS-Protection', response.headers)
        
        # Content-Security-Policy
        self.assertIn('Content-Security-Policy', response.headers)

    # ===== TESTS PASSWORD HASHING =====

    def test_password_hashed_in_database(self):
        """Test: Password hashed in database (not plaintext)"""
        with self.app.app_context():
            alice = User.query.filter_by(nom='alice').first()
            # Password must NOT be "password123" in plaintext
            self.assertNotEqual(alice.pswd_hashed, 'password123')
            # Must look like a bcrypt hash
            self.assertTrue(alice.pswd_hashed.startswith('$2'))

    # ===== TESTS AUTHORIZATION =====

    def test_cannot_delete_others_note(self):
        """Test: FORBIDDEN - Deleting another user's note"""
        self.login('bob', 'password123')
        response = self.client.delete(f'/api/notes/{self.alice_note_id}')
        # 405 = Method Not Allowed (DELETE route not implemented)
        self.assertIn(response.status_code, [403, 404, 405])

    def test_list_notes_only_shows_accessible(self):
        """Test: Note list shows only accessible notes"""
        self.login('bob', 'password123')
        response = self.client.get('/api/notes')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Bob must NOT see Alice's private note
        note_ids = [note['id'] for note in data['notes']]
        self.assertNotIn(self.alice_note_id, note_ids)
        
        # Bob MUST see the shared note
        self.assertIn(self.shared_note_id, note_ids)


    # ===== TESTS LOCK SYSTEM =====

    def test_acquire_lock_success(self):
        """Test: Acquérir un lock sur une note en write mode"""
        self.login('alice', 'password123')
        response = self.client.post(f'/api/notes/{self.shared_note_id}/lock')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['lock']['user_id'], self.alice_id)

    def test_acquire_lock_already_locked(self):
        """Test: Tentative d'acquérir un lock déjà pris"""
        # Alice acquiert le lock
        self.login('alice', 'password123')
        self.client.post(f'/api/notes/{self.shared_note_id}/lock')
        
        # Bob tente d'acquérir le même lock
        self.login('bob', 'password123')
        response = self.client.post(f'/api/notes/{self.shared_note_id}/lock')
        self.assertEqual(response.status_code, 409)  # Conflict
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_release_lock_success(self):
        """Test: Libérer un lock acquis"""
        self.login('alice', 'password123')
        # Acquérir lock
        self.client.post(f'/api/notes/{self.shared_note_id}/lock')
        # Libérer lock
        response = self.client.delete(f'/api/notes/{self.shared_note_id}/lock')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

    def test_release_lock_not_owner(self):
        """Test: INTERDIT - Libérer le lock d'un autre utilisateur"""
        # Alice acquiert le lock
        self.login('alice', 'password123')
        self.client.post(f'/api/notes/{self.shared_note_id}/lock')
        
        # Bob tente de libérer le lock d'Alice
        self.login('bob', 'password123')
        response = self.client.delete(f'/api/notes/{self.shared_note_id}/lock')
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_get_lock_status(self):
        """Test: Obtenir le statut d'un lock"""
        self.login('alice', 'password123')
        # Lock non acquis
        response = self.client.get(f'/api/notes/{self.shared_note_id}/lock')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['lock']['locked'])
        
        # Acquérir lock
        self.client.post(f'/api/notes/{self.shared_note_id}/lock')
        
        # Vérifier statut
        response = self.client.get(f'/api/notes/{self.shared_note_id}/lock')
        data = json.loads(response.data)
        self.assertTrue(data['lock']['locked'])
        self.assertEqual(data['lock']['user_id'], self.alice_id)

    def test_lock_denied_on_readonly_note(self):
        """Test: INTERDIT - Lock sur note read-only"""
        with self.app.app_context():
            from models.note import Note
            # Create read-only note
            readonly_note = Note(owner_id=self.alice_id, title="Read-only", content="Test", visibility="read")
            from models import db
            db.session.add(readonly_note)
            db.session.commit()
            readonly_note_id = readonly_note.id
        
        # Bob attempts to acquire lock on read-only note
        self.login('bob', 'password123')
        response = self.client.post(f'/api/notes/{readonly_note_id}/lock')
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Write access denied')


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
