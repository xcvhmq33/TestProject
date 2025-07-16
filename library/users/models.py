from books.models import Book
from django.contrib.auth.models import User
from django.db import models
from PIL import Image


class Profile(models.Model):
    image = models.ImageField(default="users/default_profile.png", upload_to="users")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    planned = models.ManyToManyField(Book, related_name="planned", blank=True)
    reading = models.ManyToManyField(Book, related_name="reading", blank=True)
    dropped = models.ManyToManyField(Book, related_name="dropped", blank=True)
    finished = models.ManyToManyField(Book, related_name="finished", blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
