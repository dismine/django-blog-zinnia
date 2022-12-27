"""Test urls for the zinnia project"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django_xmlrpc.views import handle_xmlrpc

from zinnia.views.channels import EntryChannel

admin.autodiscover()

urlpatterns = [
    path('', include('zinnia.urls')),
    path('channel-test/', EntryChannel.as_view(query='test')),
    path('comments/', include('django_comments.urls')),
    path('xmlrpc/', handle_xmlrpc),
    path('admin/', admin.site.urls),
]
