from django.urls import reverse_lazy

from task_manager.users.models import User
from task_manager.users.tests.testcase import UserTestCase


class TestUserListView(UserTestCase):
    def test_user_list(self):
        response = self.client.get(reverse_lazy('users:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertEqual(User.objects.count(), self.initial_user_count)


class TestUserCreateView(UserTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse_lazy('users:create')

    def test_get_create_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration_form.html')

    def test_user_creation(self):
        response = self.client.post(self.url, data=self.valid_user_data)
        self.assertEqual(User.objects.count(), self.initial_user_count + 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestUserDeleteView(UserTestCase):
    def setUp(self):
        super().setUp()
        self.delete_url = lambda pk: reverse_lazy('users:delete', 
                                                  kwargs={'pk': pk})

    def test_user_deletion_unauthorized(self):
        response = self.client.get(self.delete_url(self.user1.pk))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_user_self_deletion_authorized(self):
        self.client.force_login(self.user1)
        response = self.client.post(self.delete_url(self.user1.pk))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users:index'))
        self.assertEqual(User.objects.count(), self.initial_user_count - 1)

    def test_other_user_deletion_authorized(self):
        self.client.force_login(self.user2)
        response = self.client.post(self.delete_url(self.user1.pk))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users:index'))
        self.assertEqual(User.objects.count(), self.initial_user_count)


class TestUserUpdateView(UserTestCase):
    def setUp(self):
        super().setUp()
        self.update_url = lambda pk: reverse_lazy('users:update', 
                                                  kwargs={'pk': pk})

    def test_user_update_unauthorized(self):
        response = self.client.get(self.update_url(self.user1.pk))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_user_self_update_authorized(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            self.update_url(self.user1.pk),
            data=self.update_user_data
        )
        self.assertEqual(response.status_code, 302)
        updated_user = User.objects.get(pk=self.user1.pk)
        self.assertEqual(updated_user.username, 'high_king')

    def test_other_user_update_authorized(self):
        self.client.force_login(self.user2)
        response = self.client.post(
            self.update_url(self.user1.pk),
            data=self.update_user_data
        )
        self.assertEqual(response.status_code, 302)
        unchanged_user = User.objects.get(pk=self.user1.pk)
        self.assertEqual(unchanged_user.username, 'queen_lucy')
