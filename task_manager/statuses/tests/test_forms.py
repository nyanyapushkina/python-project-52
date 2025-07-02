from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from task_manager.statuses.tests.testcase import StatusTestCase


class TestStatusCreationForm(StatusTestCase):
    def test_valid_data(self):
        """Test valid status form data creates a status."""
        form = StatusForm(data=self.valid_status_data)
        self.assertTrue(form.is_valid())
        status = form.save()
        self.assertEqual(status.name, self.valid_status_data['name'])
        self.assertEqual(Status.objects.count(), self.status_count + 1)

    def test_missing_fields(self):
        form = StatusForm(data={
            'name': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_duplicate_name(self):
        form = StatusForm(data={
            'name': self.status1.name
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)