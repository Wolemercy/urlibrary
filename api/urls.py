from django.urls import path, re_path
from . import views

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path('books', (views.BookList.as_view()), name='book-list'),
    re_path(r'books/(?P<pk>\d+)$', views.BookRetrieveDestroy.as_view(), name='book-retrieve-destroy'),
    #api documentation
    path('docs', include_docs_urls(title='URLibraryAPI')),
    path('schema', get_schema_view(
        title="Urlibrary",
        description="A Library API",
        version="1.0.0"), 
        name='openapi-schema'),


]