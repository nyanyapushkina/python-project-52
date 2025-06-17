from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.views.generic import TemplateView

from task_manager.views import CustomLoginView, CustomLogoutView


def trigger_error(request):
    a = None
    a.hello()
    return HttpResponse("Hello, world. You're at the pollapp index.")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('users/', include('task_manager.users.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('trigger-error/', trigger_error),
]