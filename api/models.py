from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .utils import upload_to
from django.core.validators import MinValueValidator, MaxValueValidator



class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    image = models.ImageField(
        _('Image',), upload_to=upload_to, default='books/default.jpg')
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    totalPages = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    currentPage = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    reader = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-created']
