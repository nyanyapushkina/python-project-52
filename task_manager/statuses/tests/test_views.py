from django.urls import reverse_lazy

from task_manager.statuses.models import Status
from task_manager.statuses.tests.testcase import StatusTestCase


class TestStatusListView(StatusTestCase):
    def test_statuses_list_authorized(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse_lazy('statuses:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')
        self.assertEqual(Status.objects.count(), 3)
        self.assertContains(response, 'In the Wardrobe')
        self.assertContains(response, 'On Aslan\'s Side')

    def test_statuses_list_unauthorized(self):
        response = self.client.get(reverse_lazy('statuses:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestStatusCreateView(StatusTestCase):
    def test_status_creation_authorized(self):
        self.client.force_login(self.user1)
        new_status = {'name': 'At Mr. Tumnus\'s House'}

        response = self.client.post(
            reverse_lazy('statuses:create'),
            data=new_status,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 4)
        self.assertTrue(Status.objects.filter(name='At Mr. Tumnus\'s House').exists())

    def test_status_creation_unauthorized(self):
        response = self.client.post(
            reverse_lazy('statuses:create'),
            data={'name': 'Should fail'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 3)


class TestStatusUpdateView(StatusTestCase):
    def test_status_update_authorized(self):
        self.client.force_login(self.user1)
        updated_name = 'With the White Witch'

        response = self.client.post(
            reverse_lazy('statuses:update', kwargs={'pk': self.status1.id}),
            data={'name': updated_name},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.get(id=self.status1.id).name, updated_name)

    def test_status_update_unauthorized(self):
        original_name = self.status1.name
        response = self.client.post(
            reverse_lazy('statuses:update', kwargs={'pk': self.status1.id}),
            data={'name': 'Should not change'},
        )
        self.assertEqual(Status.objects.get(id=self.status1.id).name, original_name)


class TestStatusDeleteView(StatusTestCase):
    def test_status_deletion_authorized(self):
        self.client.force_login(self.user1)
        status_id = self.status1.id

        response = self.client.post(
            reverse_lazy('statuses:delete', kwargs={'pk': status_id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 2)
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(id=status_id)

    def test_status_deletion_unauthorized(self):
        status_id = self.status1.id
        self.client.post(
            reverse_lazy('statuses:delete', kwargs={'pk': status_id})
        )
        self.assertEqual(Status.objects.count(), 3)
