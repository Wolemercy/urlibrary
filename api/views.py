from django.db.models import query
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics, permissions, serializers
from rest_framework.exceptions import ValidationError
from .models import Book
from .serializers import BookSerializer

# @api_view(['GET', ])
class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reader=self.request.user)

class BookRetrieveDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        book = Book.objects.filter(pk=kwargs['pk'], reader=self.request.user)
        if book.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('This is not your book to delete!')
    
    def put(self, request, *args, **kwargs):
        book = Book.objects.filter(pk=kwargs['pk'], reader=self.request.user)
        if book.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError('This is not your book to update!')

    