from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.views import status

from api.models import Book
from django.contrib.auth.models import User

from api.serializers import BookSerializer
import json

#GET ALL BOOKS
class GetAllBooksTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        data1 = {"author": "Dan Brown",
                    "title": "Angels and Demons",
                    "totalPages": 200,
                    "currentPage": 33,
                    "reader": self.user,
                    }
        
        data2 = {"author": "Homer",
                    "title": "Odyssey",
                    "totalPages": 103,
                    "currentPage": 12,
                    "reader": self.user,
                    }
        self.book1 = Book.objects.create(**data1)
        # self.book2 = Book.objects.create(**data2)
    
    def test_get_all_books(self):
        """
        Get the list of all the books
        """
        response = self.client.get(reverse('book-list'))
        books = Book.objects.filter(reader=self.user)
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# GET SINGLE BOOK
class GetSingleBookTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        data1 = {"author": "Dan Brown",
                    "title": "Angels and Demons",
                    "totalPages": 200,
                    "currentPage": 33,
                    "reader": self.user,
                    }
        
        data2 = {"author": "Homer",
                    "title": "Odyssey",
                    "totalPages": 103,
                    "currentPage": 12,
                    "reader": self.user,
                    }
        self.book1 = Book.objects.create(**data1)
        self.book2 = Book.objects.create(**data2)
    
    def test_get_valid_single_book(self):
        """
        Ensure we can retrieve an existing book
        """
        response = self.client.get(reverse('book-retrieve-destroy', args=[self.book1.id]))
        book = Book.objects.get(pk=self.book1.id)
        serializer = BookSerializer(book)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_book(self):
        """
        Ensure we can't retrieve a non-existent book
        """
        response = self.client.get(reverse('book-retrieve-destroy', args=[3]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# POST
class CreateNewBookTest(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.valid_data = {"author": "Dan Brown",
                    "title": "Angels and Demons",
                    "totalPages": 200,
                    "currentPage": 33,
                    }
        
        self.invalid_data = {"author": "Dan Brown",
                    "title": "",
                    "totalPages": 200,
                    "currentPage": 33,
                    }
        
    def test_create_valid_book(self):
        """
        Ensure we can create a new valid book object
        """
        response = self.client.post(reverse('book-list'), self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        

    def test_book_title(self):
        """
        Ensure the created book object has the appropriate title
        """
        self.client.post(reverse('book-list'), self.valid_data)
        book1 = Book.objects.get(author="Dan Brown")
        self.assertEqual(book1.title, 'Angels and Demons')

    def test_create_invalid_book(self):
        """
        Ensure we can't create an invalid book object
        """
        response = self.client.post(reverse('book-list'), self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 0)

#PUT
class UpdateBookTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='john', email='john@snow.com', password='johnpassword')
        self.client.login(username='john', password='johnpassword')
        
        self.data = {"author": "Dan Brown",
                    "title": "Angels and Demons",
                    "totalPages": 200,
                    "currentPage": 33,
                    "reader": self.user
                    }
        self.book = Book.objects.create(**self.data)
        
        self.valid_data = {
            "author": "Dan Green",
            "title": "Angels and Demons",
            "totalPages": 200,
            "currentPage": 33,
            "reader": self.user
            }
        self.invalid_data = {
            "author": "Dan Brown",
            "title": "",
            "totalPages": 200,
            "currentPage": 33,
            "reader": self.user
            }

        
    def test_valid_update_book(self):
        """
        Ensure we can update an existing book object with a valid replacement
        """
    
        response = self.client.put(reverse('book-retrieve-destroy', args=[self.book.id]), self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_book(self):
        """
        Ensure we can't update an existing book object with an invalid replacement
        """
    
        response = self.client.put(reverse('book-retrieve-destroy', args=[self.book.id]), self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)        

#DELETE
class DeleteBookTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='john', email='john@snow.com', password='johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.data = {"author": "Dan Brown",
                    "title": "Angels and Demons",
                    "totalPages": 200,
                    "currentPage": 33,
                    "reader": self.user
                    }
        self.book = Book.objects.create(**self.data)

        
    def test_valid_delete_book(self):
        """
        Ensure we can delete an existing book object
        """
        response = self.client.delete(reverse('book-retrieve-destroy', args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
    
    def test_invalid_delete_book(self):
        """
        Ensure we cannot delete an non-existent book object
        """
        response = self.client.delete(reverse('book-retrieve-destroy', args=[2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Book.objects.count(), 1)
    

