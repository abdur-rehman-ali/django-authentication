#Celery Imports
from celery import shared_task

#Django Imports
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from decouple import config

class UserMailer:
  @staticmethod
  @shared_task
  def send_password_reset_email(user_email, link):
    subject = 'Subject of the email'
    recipient_list = [user_email]
    template = 'account/password_reset_email.html'
    context = {
      'link': link, 
      'email': user_email
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
