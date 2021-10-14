from django.db.models import query

from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie 

from .models import Book
from .serializers import BookSerializer
from django.http import Http404

class BookList(generics.ListCreateAPIView):
    
    serializer_class = BookSerializer
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return Book.objects.filter(reader=self.request.user)

    def perform_create(self, serializer):
        serializer.save(reader=self.request.user)
    
    def get_paginated_response(self, data):
       return Response(data)


class BookRetrieveDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        book = Book.objects.filter(pk=kwargs['pk'])
        if book.exists():
            book = Book.objects.filter(pk=kwargs['pk'], reader=self.request.user)
            if  book.exists():
                self.destroy(request, *args, **kwargs)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise ValidationError('This is not your book to delete!')
        else:
            raise Http404
    
    def put(self, request, *args, **kwargs):
        book = Book.objects.filter(pk=kwargs['pk'], reader=self.request.user)
        if book.exists():
            self.update(request, *args, **kwargs)
            return Response(status=status.HTTP_200_OK)
        else:
            raise ValidationError('This is not your book to update!')

    