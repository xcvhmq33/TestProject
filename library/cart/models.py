from django.contrib.auth.models import User
from django.db import models
from products.models import Product


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
