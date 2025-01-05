from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, F

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book_id = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                        Q(expected_return_date__gte=F("borrow_date"))
                        & Q(actual_return_date__gte=F("borrow_date"))
                ),
                name="return_date_gte_borrow_date",
            ),
            models.CheckConstraint(
                check=Q(
                    expected_return_date__lte=(
                            F("borrow_date") + timedelta(weeks=2)
                    )
                ),
                name="expected_return_date_within_two_weeks",
            ),
        ]

    @staticmethod
    def validate_inventory(book, error_to_raise):
        if book.inventory <= 0:
            raise error_to_raise(
                {
                    "book": f"All copies of the book '{book.title}' "
                            f"are currently unavailable for borrowing"
                }
            )

    def clean(self):
        if self.pk is None:
            Borrowing.validate_inventory(self.book_id, ValidationError)

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.full_clean()
        return super(Borrowing, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return f"{self.book_id} borrowed by {self.user_id}"
