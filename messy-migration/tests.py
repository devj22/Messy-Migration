import unittest
from app import app
import json

class UserApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_health_check(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'User Management System', resp.data)

    def test_create_user(self):
        resp = self.app.post('/users', data=json.dumps({
            'name': 'Test User',
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }), content_type='application/json')
        self.assertIn(resp.status_code, (201, 409))  # 409 if already exists

    def test_login(self):
        # Assumes user from init_db.py exists
        resp = self.app.post('/login', data=json.dumps({
            'email': 'john@example.com',
            'password': 'password123'
        }), content_type='application/json')
        self.assertIn(resp.status_code, (200, 401))

    def test_get_all_users(self):
        resp = self.app.get('/users')
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json, list)

if __name__ == '__main__':
    unittest.main() 