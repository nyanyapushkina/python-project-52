from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.labels.tests.testcase import LabelTestCase


class TestLabelCreationForm(LabelTestCase):
    def test_valid_data(self):
        form = LabelForm(data=self.valid_label_data)
        self.assertTrue(form.is_valid())
        label = form.save()
        self.assertEqual(label.name, self.valid_label_data['name'])
        self.assertEqual(Label.objects.count(), self.label_count + 1)

    def test_missing_fields(self):
        form = LabelForm(data={
            'name': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_duplicate_name(self):
        form = LabelForm(data={
            'name': self.label1.name
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)