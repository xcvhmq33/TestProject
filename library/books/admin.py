from books.models import Author, Book, Genre
from django.contrib import admin

admin.site.register([Book, Author, Genre])
