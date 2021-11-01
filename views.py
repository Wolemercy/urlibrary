
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from django.utils.translation import gettext_lazy as _

from .models import Book
from .serializers import BookSerializer
from django.http import Http404


import logging
logger_info = logging.getLogger('info')

class BookList(generics.ListCreateAPIView):
    
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """
        This view returns a list of all the books owned by
        the currently authenticated user.
        """

        if self.request.user.is_authenticated:
            logger_info.info('List of books returned')
            return Book.objects.filter(reader=self.request.user)

        else:        
            raise Http404

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

    def get_queryset(self, *args, **kwargs):
        book = Book.objects.filter(pk=self.kwargs['pk'])
        if book.exists():
            book = Book.objects.filter(pk=self.kwargs['pk'], reader=self.request.user)
            if  book.exists():
                return book
            else:
                logger_info.error('This is not your book!')
            raise Http404

        else:
            logger_info.error('This book does not exist!')
            raise Http404

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
                raise ValidationError(_('This is not your book to delete!'), code='invalid')
        else:
            logger_info.error('This book does not exist!')
            raise Http404
    
    def put(self, request, *args, **kwargs):
        book = Book.objects.filter(pk=kwargs['pk'], reader=self.request.user)
        if book.exists():
            self.update(request, *args, **kwargs)
            logger_info.info('Book updated!')
            return Response(status=status.HTTP_200_OK)
        else:
            logger_info.warning('Not your book to update!')
            raise ValidationError(_('This is not your book to update!'), code='invalid')
