"""Test urls for the zinnia project"""
from django.urls import path

from zinnia.tests.implementations.urls.default import (
    urlpatterns as test_urlpatterns)
from zinnia.views.authors import AuthorDetail
from zinnia.views.categories import CategoryDetail
from zinnia.views.tags import TagDetail


class CustomModelDetailMixin(object):
    """
    Mixin for changing the template_name
    and overriding the context.
    """
    template_name = 'zinnia/entry_custom_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'extra': 'context'})
        return context


class CustomTagDetail(CustomModelDetailMixin, TagDetail):
    pass


class CustomAuthorDetail(CustomModelDetailMixin, AuthorDetail):
    pass


class CustomCategoryDetail(CustomModelDetailMixin, CategoryDetail):
    pass


urlpatterns = [
    path('authors/<username:username>/',
        CustomAuthorDetail.as_view(),
        name='zinnia_author_detail'),
    path('authors/<username:username>/page/<int:page>/',
        CustomAuthorDetail.as_view(),
        name='zinnia_author_detail_paginated'),
    path('categories/<path:path>/page/<int:page>/',
        CustomCategoryDetail.as_view(),
        name='zinnia_category_detail_paginated'),
    path('categories/<path:path>/',
        CustomCategoryDetail.as_view(),
        name='zinnia_category_detail'),
    path('tags/<tag:tag>/',
        CustomTagDetail.as_view(),
        name='zinnia_tag_detail'),
    path('tags/<tag:tag>/page/<int:page>/',
        CustomTagDetail.as_view(),
        name='zinnia_tag_detail_paginated'),
] + test_urlpatterns
