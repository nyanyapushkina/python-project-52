from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from task_manager.views import IndexView


urlpatterns = i18n_patterns(
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    prefix_default_language=False,
)