from django.db.utils import IntegrityError

from task_manager.users.models import User
from task_manager.users.tests.testcase import UserTestCase


class TestUserModel(UserTestCase):
    def test_user_creation(self):
        initial_count = User.objects.count()
        user = User.objects.create_user(
            username='test_user',
            first_name='Test',
            last_name='User',
            password='TestPass123'  # NOSONAR
        )
        self.assertEqual(User.objects.count(), initial_count + 1)
        self.assertEqual(str(user), 'Test User')

    def test_duplicate_username(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username='queen_lucy',  # Already exists in fixtures
                first_name='Duplicate',
                last_name='User',
                password='Test123'  # NOSONAR
            )
