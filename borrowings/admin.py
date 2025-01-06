from django.contrib import admin

from borrowings.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "borrow_date",
        "actual_return_date",
        "get_book_title",
        "get_user_username"
    )

    def get_book_title(self, obj):
        return obj.book_id.title
    get_book_title.short_description = "Book Title"

    def get_user_username(self, obj):
        return obj.user_id.username
    get_user_username.short_description = "User Username"

    search_fields = ("id", "user_id__email", "book_id__title")
    ordering = ("-borrow_date", "actual_return_date")
