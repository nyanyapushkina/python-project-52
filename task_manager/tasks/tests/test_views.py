from django.urls import reverse_lazy

from task_manager.tasks.models import Task
from task_manager.tasks.tests.testcase import TaskTestCase


class TestTaskListView(TaskTestCase):
    def test_unauthorized_access_redirects_to_login(self):
        response = self.client.get(reverse_lazy('tasks'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_authorized_access_renders_task_list(self):
        self.client.force_login(self.user1)  # Lucy Pevensie
        response = self.client.get(reverse_lazy('tasks'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertEqual(len(response.context['tasks']), self.task_count)  # 2 tasks from fixtures


class TestTaskDetailView(TaskTestCase):
    def test_redirects_unauthorized_user(self):
        response = self.client.get(
            reverse_lazy('tasks:detail', kwargs={'pk': self.task1.id})  # "Defeat the White Witch"
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_renders_detail_for_authorized_user(self):
        self.client.force_login(self.user1)  # Lucy Pevensie
        response = self.client.get(
            reverse_lazy('tasks:detail', kwargs={'pk': self.task1.id})  # "Defeat the White Witch"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertEqual(response.context['task'], self.task1)

    def test_404_for_nonexistent_task(self):
        self.client.force_login(self.user1)  # Lucy Pevensie
        response = self.client.get(
            reverse_lazy('tasks:detail', kwargs={'pk': 9999})
        )
        self.assertEqual(response.status_code, 404)


class TestTaskCreateView(TaskTestCase):
    def test_redirects_unauthenticated_user(self):
        response = self.client.get(reverse_lazy('tasks:create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('tasks:create'), data=self.valid_task_data  # "Find Mr. Tumnus"
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_creates_task_for_logged_in_user(self):
        self.client.force_login(self.user1)  # Lucy Pevensie
        initial_count = Task.objects.count()  # 2 from fixtures

        response = self.client.get(reverse_lazy('tasks:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')

        response = self.client.post(
            reverse_lazy('tasks:create'),
            data=self.valid_task_data  # "Find Mr. Tumnus"
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))
        self.assertEqual(Task.objects.count(), initial_count + 1)  # Now 3 tasks

        # Verify author was automatically set
        new_task = Task.objects.latest('created_at')
        self.assertEqual(new_task.author, self.user1)  # Lucy should be author


class TestTaskUpdateView(TaskTestCase):
    def test_redirects_unauthenticated_user(self):
        response = self.client.get(
            reverse_lazy('tasks:update', kwargs={'pk': self.task1.id})  # "Defeat the White Witch"
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('tasks:update', kwargs={'pk': self.task1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_logged_in_user_can_update_task(self):
        self.client.force_login(self.user1)  # Lucy Pevensie
        update_data = self.update_task_data.copy()  # "Attend the Coronation"
        update_data['name'] = 'Updated: Defeat the Witch'

        response = self.client.get(
            reverse_lazy('tasks:update', kwargs={'pk': self.task1.id})  # "Defeat the White Witch"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')

        response = self.client.post(
            reverse_lazy('tasks:update', kwargs={'pk': self.task1.id}),
            data=update_data
        )
        self.assertRedirects(response, reverse_lazy('tasks'))
        updated_task = Task.objects.get(id=self.task1.id)
        self.assertEqual(updated_task.name, update_data['name'])


class TestTaskDeleteView(TaskTestCase):
    def test_redirects_unauthenticated_user(self):
        response = self.client.get(
            reverse_lazy('tasks:delete', kwargs={'pk': self.task1.id})  # "Defeat the White Witch"
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('tasks:delete', kwargs={'pk': self.task1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_owner_can_delete_task(self):
        self.client.force_login(self.user1)  # Lucy (author of task1)
        initial_count = Task.objects.count()  # 2 from fixtures

        response = self.client.get(
            reverse_lazy('tasks:delete', kwargs={'pk': self.task1.id})  # "Defeat the White Witch"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_confirm_delete.html')

        response = self.client.post(
            reverse_lazy('tasks:delete', kwargs={'pk': self.task1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))
        self.assertEqual(Task.objects.count(), initial_count - 1)  # Now 1 task

        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task1.id)

    def test_non_author_cannot_delete_task(self):
        self.client.force_login(self.user2)  # Edmund (not author of task1)
        initial_count = Task.objects.count()  # 2 from fixtures

        response = self.client.get(
            reverse_lazy('tasks:delete', kwargs={'pk': self.task1.id})  # "Defeat the White Witch"
        )
        self.assertEqual(response.status_code, 302)  # Redirects instead of showing form
        self.assertRedirects(response, reverse_lazy('tasks'))

        response = self.client.post(
            reverse_lazy('tasks:delete', kwargs={'pk': self.task1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))
        self.assertEqual(Task.objects.count(), initial_count)  # Still 2 tasks
        unchanged_task = Task.objects.get(id=self.task1.id)
        self.assertEqual(unchanged_task.name, self.task1.name)