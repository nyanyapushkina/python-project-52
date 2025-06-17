from django.test import Client, TestCase

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskTestCase(TestCase):
    fixtures = ['test_users.json',
                'test_statuses.json',
                'test_labels.json',
                'test_tasks.json']

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.get(pk=1)  # Lucy Pevensie
        self.user2 = User.objects.get(pk=2)  # Edmund Pevensie

        self.status1 = Status.objects.get(pk=1)  # In the Wardrobe
        self.status2 = Status.objects.get(pk=2)  # On Aslan's Side

        self.label1 = Label.objects.get(pk=1)  # Battle
        self.label2 = Label.objects.get(pk=2)  # Magic

        self.task1 = Task.objects.get(pk=1)  # Defeat the White Witch
        self.task2 = Task.objects.get(pk=2)  # Repair the Lamppost

        self.task1.labels.set([self.label1])
        self.task2.labels.set([self.label1, self.label2])

        self.task_count = Task.objects.count()

        self.valid_task_data = {
            'name': 'Find Mr. Tumnus',
            'description': 'Search for the faun in the snowy woods',
            'status': self.status1.id,
            'executor': self.user1.id,
            'labels': [self.label1.id, self.label2.id]
        }

        self.update_task_data = {
            'name': 'Attend the Coronation',
            'description': 'Become the Queen of Narnia',
            'status': self.status2.id,
            'executor': self.user2.id,
            'labels': [self.label1.id]
        }
    
    def assertFilteredTasksCount(self, response, expected_count, msg=None):
        self.assertEqual(response.status_code, 200, msg)
        if hasattr(response.context, 'filter'):
            self.assertEqual(len(response.context['filter'].qs), 
                             expected_count, msg)
        else:
            self.fail("Response context doesn't contain 'filter' object")