import unittest
from app.models import User
from app import create_app, db
from app.models import Role, AnonymousUser, Permission

class UserModelTestCase(unittest.TestCase):

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

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_get(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_are_random(self):
        u1 = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u1.password_hash != u2.password_hash)

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

    def test_roles_and_permissions(self):
        Role.insert_roles()
        user = User(email='test@test.com', password='cat')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.can(Permission.WRITE_ARTICLES))
        self.assertFalse(user.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))

