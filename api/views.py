from django.db.models import query

from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


from .models import Book
from .serializers import BookSerializer
from django.http import Http404

from rest_framework.parsers import MultiPartParser, FormParser

import logging, traceback
logger_info = logging.getLogger('info')

class BookList(generics.ListCreateAPIView):
    
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        logger_info.info('List of books returned')
        return Book.objects.filter(reader=self.request.user)

    def perform_create(self, serializer):
        serializer.save(reader=self.request.user)
        logger_info.info('New book created')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_paginated_response(self, data):
       return Response(data, status=status.HTTP_200_OK)


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
                logger_info.info('Book deleted!')
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                logger_info.warning('Not your book to delete!')
                raise ValidationError('This is not your book to delete!')
        else:
            logger_info.error('Not your book to delete!')
            raise Http404
    
    def put(self, request, *args, **kwargs):
        book = Book.objects.filter(pk=kwargs['pk'], reader=self.request.user)
        if book.exists():
            self.update(request, *args, **kwargs)
            logger_info.info('Book updated!')
            return Response(status=status.HTTP_200_OK)
        else:
            logger_info.warning('Not your book to update!')
            raise ValidationError('This is not your book to update!')

    