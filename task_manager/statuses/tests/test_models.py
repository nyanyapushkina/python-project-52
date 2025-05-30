from task_manager.statuses.models import Status
from task_manager.statuses.tests.testcase import StatusTestCase


class TestStatusModel(StatusTestCase):
    def create_test_status(self, **overrides):
        """Helper to create a status with optional overrides."""
        status_data = {
            'name': 'At the Stone Table',
        }
        status_data.update(overrides)
        return Status.objects.create(**status_data)

    def test_status_creation(self):
        initial_count = Status.objects.count()
        status = self.create_test_status()
        self.assertEqual(Status.objects.count(), initial_count + 1)

        db_status = Status.objects.get(pk=status.pk)
        self.assertEqual(db_status.name, 'At the Stone Table')
        self.assertIsNotNone(db_status.created_at)
        self.assertEqual(str(db_status), 'At the Stone Table')

    def test_duplicate_status_name(self):
        with self.assertRaises(Exception):
            self.create_test_status(name='In the Wardrobe')

    def test_blank_status_name(self):
        status = Status(name='')
        with self.assertRaises(Exception):
            status.full_clean()
