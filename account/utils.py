#Local Imports
from account.models import User

from rest_framework_simplejwt.tokens import RefreshToken

def get_user_by_email(email):
  users = User.objects.filter(email=email)
  if users.exists():
    return users.first()
  return None


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
    'refresh': str(refresh),
    'access': str(refresh.access_token),
  }
