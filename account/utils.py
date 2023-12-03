#Django Imports
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from decouple import config

#Local Imports
from account.models import User

def get_user_by_email(email):
  users = User.objects.filter(email=email)
  if users.exists():
    return users.first()
  return None


def send_password_reset_email(user, link):
  subject = 'Subject of the email'
  recipient_list = [user]
  template = 'account/password_reset_email.html'
  context = {
    'link': link, 
    'user': user
  }
  message = render_to_string(template, context)
  email = EmailMessage(
    subject=subject,
    body=message,
    from_email=config('EMAIL_ADDRESS'),
    to=recipient_list
  )
  email.content_subtype = 'html'
  email.send()
