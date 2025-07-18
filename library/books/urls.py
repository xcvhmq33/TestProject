from books.views import BookDetailView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path("<slug:slug>", BookDetailView.as_view(), name="book-detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
