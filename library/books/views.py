from books.models import Book
from django.views.generic import DetailView


class BookDetailView(DetailView):
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"
