from books.models import Book
from django.views.generic import DetailView, ListView


class BookListView(ListView):
    model = Book
    template_name = "book/book_list.html"
    context_object_name = "books"


class BookDetailView(DetailView):
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"
