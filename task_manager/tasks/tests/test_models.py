from django.utils.timezone import now

from task_manager.tasks.models import Task
from task_manager.tasks.tests.testcase import TaskTestCase


class TestTaskModel(TaskTestCase):
    def test_task_creation_with_labels_and_executor(self):
        task = Task.objects.create(
            name=self.valid_task_data['name'],  # "Find Mr. Tumnus"
            description=self.valid_task_data['description'],  # "Search for the faun..."
            status=self.status1,  # "In the Wardrobe"
            executor=self.user1,  # Lucy
            author=self.user2,  # Edmund
        )
        task.labels.set([self.label1, self.label2])  # "Battle" and "Magic"

        self.assertEqual(task.name, self.valid_task_data['name'])
        self.assertEqual(task.description, self.valid_task_data['description'])
        self.assertEqual(task.author, self.user2)  # Edmund
        self.assertEqual(task.executor, self.user1)  # Lucy
        self.assertEqual(task.status, self.status1)  # "In the Wardrobe"
        self.assertSetEqual(set(task.labels.all()), {self.label1, self.label2})
        self.assertEqual(str(task), self.valid_task_data['name'])
        self.assertIsNotNone(task.created_at)
        self.assertLessEqual(task.created_at, now())

    def test_task_creation_with_blank_fields(self):
        task = Task.objects.create(
            name=self.valid_task_data['name'],  # "Find Mr. Tumnus"
            status=self.status1,  # "In the Wardrobe"
            author=self.user2,  # Edmund
        )
        self.assertIsNone(task.executor)
        self.assertEqual(task.labels.count(), 0)

    def test_unique_name(self):
        Task.objects.create(
            name=self.valid_task_data['name'],  # "Find Mr. Tumnus"
            status=self.status1,  # "In the Wardrobe"
            author=self.user2,  # Edmund
        )
        with self.assertRaises(Exception):
            Task.objects.create(
                name=self.valid_task_data['name'],  # "Find Mr. Tumnus"
                status=self.status1,  # "In the Wardrobe"
                author=self.user2,  # Edmund
            )