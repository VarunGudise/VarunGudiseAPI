import unittest
from flask import Flask
from api import app, db, UserModel, ThingModel

class APITestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        """Test POST /api/users/"""
        response = self.app.post('/api/users/', 
            json={'name': 'John Doe', 'email': 'john@example.com'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json[0]['name'], 'John Doe')
        self.assertEqual(response.json[0]['email'], 'john@example.com')

    def test_get_users(self):
        """Test GET /api/users/"""
        with app.app_context():
            user = UserModel(name='Jane Doe', email='jane@example.com')
            db.session.add(user)
            db.session.commit()
        response = self.app.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], 'Jane Doe')

    def test_get_user(self):
        """Test GET /api/users/<id>"""
        with app.app_context():
            user = UserModel(name='Test User', email='test@example.com')
            db.session.add(user)
            db.session.commit()
            user_id = user.id
        response = self.app.get(f'/api/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test User')

    def test_update_user(self):
        """Test PATCH /api/users/<id>"""
        with app.app_context():
            user = UserModel(name='Old Name', email='old@example.com')
            db.session.add(user)
            db.session.commit()
            user_id = user.id
        response = self.app.patch(f'/api/users/{user_id}', 
            json={'name': 'New Name', 'email': 'new@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'New Name')
        self.assertEqual(response.json['email'], 'new@example.com')

    def test_delete_user(self):
        """Test DELETE /api/users/<id>"""
        with app.app_context():
            user = UserModel(name='Delete Me', email='delete@example.com')
            db.session.add(user)
            db.session.commit()
            user_id = user.id
        response = self.app.delete(f'/api/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)

    def test_create_thing(self):
        """Test POST /api/things/"""
        with app.app_context():
            user = UserModel(name='Owner', email='owner@example.com')
            db.session.add(user)
            db.session.commit()
            user_id = user.id
        response = self.app.post('/api/things/', 
            json={'name': 'Test Thing', 'owner_id': user_id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json[0]['name'], 'Test Thing')
        self.assertEqual(response.json[0]['owner_id'], user_id)

    def test_get_things(self):
        """Test GET /api/things/"""
        with app.app_context():
            user = UserModel(name='Owner', email='owner@example.com')
            db.session.add(user)
            db.session.commit()
            thing = ThingModel(name='Test Thing', owner_id=user.id)
            db.session.add(thing)
            db.session.commit()
        response = self.app.get('/api/things/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], 'Test Thing')

    def test_get_thing(self):
        """Test GET /api/things/<id>"""
        with app.app_context():
            user = UserModel(name='Owner', email='owner@example.com')
            db.session.add(user)
            db.session.commit()
            thing = ThingModel(name='Test Thing', owner_id=user.id)
            db.session.add(thing)
            db.session.commit()
            thing_id = thing.id
        response = self.app.get(f'/api/things/{thing_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test Thing')
        self.assertEqual(response.json['id'], thing_id)

def test_update_thing(self):
    """Test PATCH /api/things/<id>"""
    with app.app_context():
        user = UserModel(name='Owner', email='owner@example.com')
        db.session.add(user)
        db.session.commit()
        thing = ThingModel(name='Old Thing', owner_id=user.id)
        db.session.add(thing)
        db.session.commit()
        thing_id = thing.id
        response = self.app.patch(f'/api/things/{thing_id}', 
            json={'name': 'New Thing', 'owner_id': user.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'New Thing')

    def test_delete_thing(self):
        """Test DELETE /api/things/<id>"""
        with app.app_context():
            user = UserModel(name='Owner', email='owner@example.com')
            db.session.add(user)
            db.session.commit()
            thing = ThingModel(name='Delete Thing', owner_id=user.id)
            db.session.add(thing)
            db.session.commit()
            thing_id = thing.id
        response = self.app.delete(f'/api/things/{thing_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)

    def test_get_nonexistent_user(self):
        """Test GET /api/users/<id> with invalid ID"""
        response = self.app.get('/api/users/999')
        self.assertEqual(response.status_code, 404)

    def test_get_nonexistent_thing(self):
        """Test GET /api/things/<id> with invalid ID"""
        response = self.app.get('/api/things/999')
        self.assertEqual(response.status_code, 404)

    def test_create_thing_invalid_owner(self):
        """Test POST /api/things/ with invalid owner_id"""
        response = self.app.post('/api/things/', 
            json={'name': 'Test Thing', 'owner_id': 999})
        self.assertEqual(response.status_code, 400)

    def test_update_thing_invalid_owner(self):
        """Test PATCH /api/things/<id> with invalid owner_id"""
        with app.app_context():
            user = UserModel(name='Owner', email='owner@example.com')
            db.session.add(user)
            db.session.commit()
            thing = ThingModel(name='Test Thing', owner_id=user.id)
            db.session.add(thing)
            db.session.commit()
            thing_id = thing.id
        response = self.app.patch(f'/api/things/{thing_id}', 
            json={'name': 'New Thing', 'owner_id': 999})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()