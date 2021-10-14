from django.urls import path, re_path
from . import views

from django.views.decorators.cache import cache_page

urlpatterns = [
    path('books', cache_page(60*60*2)(views.BookList.as_view()), name='book-list'),
    re_path(r'books/(?P<pk>\d+)/$', views.BookRetrieveDestroy.as_view(), name='book-retrieve-destroy'),

]