from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'author',
                    'executor', 'created_at', 'get_labels')
    search_fields = ['name', 'description', 
                     'author__username', 'executor__username']
    list_filter = ['status', 'author', 'executor', 'labels', 'created_at']
    filter_horizontal = ('labels',)
    ordering = ('-created_at',)

    @admin.display(description=_('Labels'))
    def get_labels(self, obj):
        return ', '.join([label.name for label in obj.labels.all()])


admin.site.register(Task, TaskAdmin)