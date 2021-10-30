from django.urls import path, re_path, include
from . import views

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    #books
    path('books', (views.BookList.as_view()), name='book-list'),
    re_path(r'books/(?P<pk>\d+)', views.BookRetrieveDestroy.as_view(), name='book-retrieve-destroy'),

    #auth
    path('dj-rest-auth/', include('dj_rest_auth.urls'), name=),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    #auth

    #request token
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    #api documentation
    path('docs', include_docs_urls(title='URLibraryAPI')),
    path('schema', get_schema_view(
        title="Urlibrary",
        description="A Library API",
        version="1.0.0"), 
        name='openapi-schema'),


]