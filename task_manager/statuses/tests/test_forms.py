from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from task_manager.statuses.tests.testcase import StatusTestCase


class TestStatusCreationForm(StatusTestCase):
    def test_valid_data(self):
        """Test valid status form data creates a status."""
        form = StatusForm(data={'name': 'At the Lamp-post'})
        self.assertTrue(form.is_valid())
        status = form.save()
        self.assertEqual(status.name, 'At the Lamp-post')
        self.assertEqual(Status.objects.count(), self.status_count + 1)

    def test_missing_fields(self):
        form = StatusForm(data={'name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_duplicate_name(self):
        form = StatusForm(data={'name': self.status1.name})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class TestStatusModel(StatusTestCase):
    def create_test_status(self, **overrides):
        """Helper to create a status with optional overrides."""
        status_data = {'name': 'In the Lantern Waste'}
        status_data.update(overrides)
        return Status.objects.create(**status_data)

    def test_status_creation(self):
        initial_count = Status.objects.count()
        status = self.create_test_status()
        self.assertEqual(Status.objects.count(), initial_count + 1)

        db_status = Status.objects.get(pk=status.pk)
        self.assertEqual(db_status.name, 'In the Lantern Waste')
        self.assertIsNotNone(db_status.created_at)
        self.assertEqual(str(db_status), 'In the Lantern Waste')

    def test_duplicate_status_name(self):
        self.create_test_status(name='Duplicate')
        with self.assertRaises(Exception):
            self.create_test_status(name='Duplicate')

    def test_blank_status_name(self):
        status = Status(name='')
        with self.assertRaises(Exception):
            status.full_clean()
