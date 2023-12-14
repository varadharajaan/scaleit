import unittest
from flask_testing import TestCase
from autoscaler import app, db, User, Role
from flask_login import current_user


class TestYourApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        user = User(username='testuser', password='testpassword')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login(self):
        response = self.client.post('/login', json={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful', response.json['message'])

    def test_get_status(self):
        response = self.client.get('/app/status')
        self.assertEqual(response.status_code, 401)  # Unauthorized without login

        self.login('testuser', 'testpassword')
        response = self.client.get('/app/status')
        self.assertEqual(response.status_code, 200)
        self.assertIn('highPriority', response.json['cpu'])
        self.assertIn('replicas', response.json)

    def test_update_replicas_without_authentication(self):
        response = self.client.put('/app/replicas', json={'replicas': 5})
        self.assertEqual(response.status_code, 401)

    def test_update_replicas(self):
        response = self.client.put('/app/replicas', json={'replicas': 5})
        self.assertEqual(response.status_code, 401)  # Unauthorized without login

        # Log in the user
        self.login('testuser', 'testpassword')

        # Assign admin role to the user
        current_user.roles.append(Role(name='admin'))
        db.session.commit()

        response = self.client.put('/app/replicas', json={'replicas': 5})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Replica count updated', response.json['message'])

    def login(self, username, password):
        return self.client.post('/login', json={'username': username, 'password': password})


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestYourApp)
    unittest.TextTestRunner(verbosity=2).run(suite)
