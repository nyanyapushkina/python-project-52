from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.tasks.tests.testcase import TaskTestCase


class TestTaskForm(TaskTestCase):
    def test_valid_data(self):
        user2 = self.user2
        form = TaskForm(data=self.valid_task_data)
        self.assertTrue(form.is_valid())
        task = form.save(commit=False)
        task.author = user2
        task.save()
        form.save_m2m()

        self.assertEqual(Task.objects.count(), self.task_count + 1)
        self.assertEqual(task.name, self.valid_task_data['name'])
        self.assertEqual(task.executor, self.user1)
        self.assertEqual(task.status, self.status1)
        self.assertSetEqual(set(task.labels.all()), {self.label1, self.label2})

    def test_missing_fields(self):
        invalid_data = self.valid_task_data.copy()
        invalid_data.update({
            'name': '',
            'status': '',
        })
        form = TaskForm(invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('status', form.errors)

    def test_blank_fields(self):
        test_data = self.valid_task_data.copy()
        test_data.update({
            'description': '',
            'executor': '',
            'labels': [],
        })
        form = TaskForm(data=test_data)
        self.assertTrue(form.is_valid())

        user2 = self.user2
        task = form.save(commit=False)
        task.author = user2
        task.save()
        self.assertEqual(task.labels.count(), 0)

    def test_duplicate_name(self):
        user2 = self.user2
        form1 = TaskForm(data=self.valid_task_data)
        task = form1.save(commit=False)
        task.author = user2
        task.save()

        duplicate_data = self.valid_task_data.copy()
        form2 = TaskForm(data=duplicate_data)
        self.assertFalse(form2.is_valid())
        self.assertIn('name', form2.errors)
