from task_manager.users.models import User
from task_manager.users.tests.testcase import UserTestCase


class TestUserModel(UserTestCase):
    def create_test_user(self, **overrides):
        """Helper to create a user with overrides."""
        user_data = {
            'first_name': self.valid_user_data['first_name'],
            'last_name': self.valid_user_data['last_name'],
            'username': self.valid_user_data['username'],
            'password': self.valid_user_data['password1'],
        }
        user_data.update(overrides)
        return User.objects.create_user(**user_data)

    def test_user_creation(self):
        initial_count = User.objects.count()
        self.create_test_user()
        self.assertEqual(User.objects.count(), initial_count + 1)

        db_user = User.objects.get(username=self.valid_user_data['username'])
        self.assertEqual(db_user.username, 'queen_lucy')
        self.assertEqual(db_user.first_name, 'Lucy')
        self.assertEqual(db_user.last_name, 'Pevensie')
        self.assertTrue(db_user.check_password('Valiant123'))
        self.assertEqual(str(db_user), 'Lucy Pevensie')

    def test_duplicate_username(self):
        self.create_test_user()
        with self.assertRaises(Exception):
            self.create_test_user(
                first_name='Edmund',
                last_name='Pevensie',
                username='queen_lucy',
                password='JustKing123'
            )
