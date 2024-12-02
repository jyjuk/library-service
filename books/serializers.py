from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "daily_fee",
            "inventory",
            "cover",
            "author",
            "title",
        ]
