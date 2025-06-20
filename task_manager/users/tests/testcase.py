from django.test import Client, TestCase

from task_manager.users.models import User


class UserTestCase(TestCase):
    """
    Base test case for user-related tests.
    Loads initial users from fixtures and provides common test data.
    """
    fixtures = ['task_manager/fixtures/test_users.json']

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.get(username='queen_lucy')
        self.user2 = User.objects.get(username='king_edmund')

        self.initial_user_count = User.objects.count()

        self.valid_user_data = {
            'first_name': 'Lucy',
            'last_name': 'Pevensie',
            'username': 'new_queen',
            'password1': 'Valiant123!',  # NOSONAR
            'password2': 'Valiant123!'   # NOSONAR
        }

        self.update_user_data = {
            'first_name': 'Peter',
            'last_name': 'Pevensie',
            'username': 'high_king',
            'password1': 'Magnificent456!',  # NOSONAR
            'password2': 'Magnificent456!'   # NOSONAR
        }
