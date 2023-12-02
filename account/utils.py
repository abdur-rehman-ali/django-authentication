#Local Imports
from account.models import User

def get_user_by_email(email):
  users = User.objects.filter(email=email)
  if users.exists():
    return users.first()
  return None
