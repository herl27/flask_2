import unittest
from app.models import User
from app import create_app, db

class UserModelConfirmTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.u1 = User(username='test1')
        self.u2 = User(username='test2')
        db.session.add_all([self.u1, self.u2])
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_confirmed_default(self):
        self.assertFalse(self.u1.confirmed)

    def test_confirm_false(self):
        self.token = self.u1.generate_confirmation_token()
        self.assertFalse(self.u2.confirm(self.token))
        self.assertFalse(self.u2.confirmed)

    def test_confirm_true(self):
        self.token = self.u1.generate_confirmation_token()
        self.assertTrue(self.u1.confirm(self.token))
        self.assertTrue(self.u1.confirmed)

