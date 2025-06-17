import django_filters

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        field_name='status__name',
        queryset=Status.objects.all(),
        label='Status'
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Executor'
    )
    labels = django_filters.ModelChoiceFilter(
        field_name='labels__name',
        queryset=Label.objects.all(),
        label='Label'
    )
    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label='My tasks only'
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
