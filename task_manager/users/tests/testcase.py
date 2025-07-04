from django.test import Client, TestCase

from task_manager.users.models import User


class UserTestCase(TestCase):
    fixtures = ['test_users.json']

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)

        self.user_count = User.objects.count()

        self.valid_user_data = {
            'first_name': 'Susan',
            'last_name': 'Pevensie',
            'username': 'queen_susan',
            'password1': 'Gentle123',
            'password2': 'Gentle123'
        }

        self.update_user_data = {
            'first_name': 'Peter',
            'last_name': 'Pevensie',
            'username': 'high_king',
            'password1': 'Magnificent456',
            'password2': 'Magnificent456'
        }
