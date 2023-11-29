#Django Imports
from django.urls import path

#Local Imprts
from account.views import (
  UserRegistrationView,
  UserLoginView
)

urlpatterns = [
  path('register', UserRegistrationView.as_view()),
  path('login', UserLoginView.as_view()),
]
