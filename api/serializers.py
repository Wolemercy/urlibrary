from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Book
import math


class BookSerializer(serializers.ModelSerializer):
    reader = serializers.ReadOnlyField(source='reader.username')
    reader_id = serializers.ReadOnlyField(source='reader.id')
    reading_progress = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'image', 'reader', 'reader_id',
                  'created', 'totalPages', 'currentPage', 'reading_progress']

    def get_reading_progress(self, book):
        if not book.totalPages:
            return "N/A"
        else:
            progress = math.floor(100 * (book.currentPage / book.totalPages))
            return str(progress) + '%'
