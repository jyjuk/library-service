from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id"
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book_id = serializers.StringRelatedField()
    user_id = serializers.StringRelatedField()
    actual_return_date = serializers.DateField(required=False)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id"
        )
        read_only_fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book_id",
            "user_id"
        )

    def validate(self, attrs):
        data = super(BorrowingDetailSerializer, self).validate(attrs=attrs)
        if self.instance.actual_return_date:
            raise serializers.ValidationError(
                "This borrowing has already been returned."
            )
        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.actual_return_date = validated_data.get(
            "actual_return_date",
            instance.actual_return_date
        )

        instance.save()

        instance.refresh_from_db()
        book = instance.book_id
        book.inventory += 1
        book.save()
        return instance


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "expected_return_date",
            "book_id"
        )

    def validate(self, attrs):
        data = super(BorrowingCreateSerializer, self).validate(attrs=attrs)
        Borrowing.validate_inventory(attrs["book_id"], ValidationError)
        return data

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        borrowing = Borrowing.objects.create(
            expected_return_date=validated_data['expected_return_date'],
            book_id=validated_data['book_id'],
            user_id=user
        )

        book = validated_data.get("book_id")
        book.inventory -= 1
        book.save()
        return borrowing
