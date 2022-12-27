"""Poor test urls for the zinnia project"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from zinnia.views.entries import EntryDetail

admin.autodiscover()

blog_urls = ([
    path('<yyyy:year>/<mm:month>/<dd:day>/<slug:slug>/',
        EntryDetail.as_view(),
        name='entry_detail')],
    'zinnia'
)

urlpatterns = [
    path('', include(blog_urls)),
    path('admin/', admin.site.urls),
]
