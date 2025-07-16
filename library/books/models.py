from django.db import models


class Author(models.Model):
    fullname = models.CharField("ФИО", max_length=255)
    image = models.ImageField(
        "Изображение", default="authors/default_author.png", upload_to="books"
    )

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Genre(models.Model):
    name = models.CharField("Название", max_length=127, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Book(models.Model):
    title = models.CharField("Название", max_length=127)
    slug = models.SlugField(max_length=127)
    image = models.ImageField(
        "Изображение", default="books/default_book.png", upload_to="books"
    )
    summary = models.TextField("Кратко")
    publication_date = models.DateField("Дата публикации")

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
