from django.urls import path
from .views import UserViewSet

urlpatterns = [
  path('user/register', UserViewSet.as_view(), name="register"),
  path('user',  UserViewSet.as_view(), name="user_list")
]
