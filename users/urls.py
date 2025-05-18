from django.urls import path
from .views import UserListView, UserCreateView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('', UserListView.as_view(), name='users'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<int:id>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:id>/delete/', UserDeleteView.as_view(), name='user_delete'),
]