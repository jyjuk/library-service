from django.db import models


class Book(models.Model):
    class Cover(models.TextChoices):
        SOFT = "1", "SOFT"
        HARD = "2", "HARD"
    daily_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Daily rental fee for the book"
    )
    inventory = models.PositiveIntegerField(
        help_text="Number of copies available"
    )
    cover = models.CharField(
        choices=Cover.choices,
        max_length=2,
        help_text="Type of book cover"
    )
    author = models.CharField(max_length=255, help_text="Author of the book")
    title = models.CharField(max_length=255, help_text="Title of the book")

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"{self.title} - {self.author} : {self.inventory} pcs"
