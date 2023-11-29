#Django Imports
from django.urls import path

#Local Imprts
from account.views import UserRegistrationView

urlpatterns = [
  path('register', UserRegistrationView.as_view()),
]
