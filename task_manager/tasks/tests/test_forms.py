from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.tasks.tests.testcase import TaskTestCase


class TestTaskForm(TaskTestCase):
    def test_valid_data(self):
        lucy = self.user1  # Lucy Pevensie
        form = TaskForm(data={
            'name': 'Find Mr. Tumnus',
            'description': 'Search for the faun in the snowy woods',
            'status': self.status1.id,  # In the Wardrobe
            'executor': self.user2.id  # Edmund Pevensie
        })
        self.assertTrue(form.is_valid())
        task = form.save(commit=False)
        task.author = lucy
        task.save()

        self.assertEqual(Task.objects.count(), self.task_count + 1)
        self.assertEqual(task.name, 'Find Mr. Tumnus')
        self.assertEqual(task.executor, self.user2)  # Edmund
        self.assertEqual(task.status, self.status1)  # In the Wardrobe
        self.assertEqual(task.author, lucy)  # Lucy is the author

    def test_missing_required_fields(self):
        form = TaskForm(data={
            'name': '',  # Required field
            'description': 'Some description',
            'status': '',  # Required field
            'executor': self.user1.id
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('status', form.errors)

    def test_optional_fields(self):
        """Test that description and executor are optional."""
        form = TaskForm(data={
            'name': 'Have tea with Mr. Tumnus',
            'description': '',  # Optional
            'status': self.status1.id,
            'executor': ''  # Optional
        })
        self.assertTrue(form.is_valid())

    def test_executor_queryset(self):
        form = TaskForm()
        self.assertEqual(
            set(form.fields['executor'].queryset),
            {self.user1, self.user2}
        )
        # Test that only specific fields are selected
        self.assertFalse(hasattr(form.fields['executor'].queryset.first(), 
                                 'password'))

    def test_status_queryset(self):
        form = TaskForm()
        self.assertEqual(
            set(form.fields['status'].queryset),
            {self.status1, self.status2}
        )
        self.assertFalse(hasattr(form.fields['status'].queryset.first(), 
                                 'created_at'))

    def test_form_labels(self):
        form = TaskForm()
        self.assertEqual(form.fields['executor'].label, 'Assignee')
        self.assertEqual(form.fields['description'].widget.attrs['rows'], 3)