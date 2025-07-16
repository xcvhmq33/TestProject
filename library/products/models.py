from django.db import models
from books.models import Book

class Product(models.Model):
    price = models.DecimalField("Стоимость", max_digits=100, decimal_places=2)
    stock = models.PositiveIntegerField("На складе")
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="products")

    class Meta:
        ordering = ("book",)
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.book.title
