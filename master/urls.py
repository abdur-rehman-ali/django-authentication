from django.contrib import admin
from django.urls import path, include

urlpatterns = [
  path('admin/', admin.site.urls),
  path('api/v1/', include('account.urls')),
  path('mailer/', include('django_mail_viewer.urls')),
  path('schema-viewer/', include('schema_viewer.urls')),
]
