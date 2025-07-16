from books.views import BookDetailView, BookListView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path("", BookListView.as_view(), name="book-list"),
    path("<slug:slug>", BookDetailView.as_view(), name="book-detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
