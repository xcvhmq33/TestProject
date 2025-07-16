from books.models import Book
from django.contrib.auth.models import User
from django.db import models


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


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        unique_together = ("user", "product")
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.book.title} x {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    full_name = models.CharField("ФИО", max_length=255)
    email = models.EmailField("Почта")
    address = models.TextField("Адрес")
    city = models.CharField("Город", max_length=127)
    postal_code = models.CharField("Почтовый индекс", max_length=20)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Status(models.TextChoices):
        NEW = "new", "Новый"
        PROCESSING = "processing", "В обработке"
        COMPLETED = "completed", "Завершён"
        CANCELLED = "cancelled", "Отменён"

    status = models.CharField(
        "Статус", max_length=20, choices=Status.choices, default="new"
    )

    def __str__(self):
        return f"Заказ #{self.id} - {self.full_name}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField("Количество")
    price = models.DecimalField("Стоимость", max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.book.title} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
