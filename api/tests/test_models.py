# from django.test import TestCase
# from api.models import Book
# from django.contrib.auth.models import User


# class BookTestCase(TestCase):

#     def setUp(self) -> None:
#         reader = User.objects.create_user(username='Phil')

#         Book.objects.create(title='Brave New World',
#                             author='Aldous Huxley',
#                             currentPage=15,
#                             totalPages = 120,
#                             reader = reader
#                             )
#         Book.objects.create(title='Paradise Lost',
#                             author='John Milton',
#                             currentPage=28,
#                             totalPages = 95,
#                             reader = reader
#                             )
    
#     def test_author_name_is_correct(self): 
#         """
#         Ensure books have appropriate author names
#         """
#         book1 = Book.objects.get(title='Brave New World')

#         self.assertEqual(book1.author, 'Aldous Huxley')

#     def test_author_name_is_wrong(self): 
#         """
#         Ensure books with inappropriate author names are flagged
#         """
#         book2 = Book.objects.get(title='Paradise Lost')

#         self.assertNotEqual(book2.author, 'John Boyega')




        