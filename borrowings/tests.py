from datetime import datetime
import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.tests import sample_book
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
)


BORROWING_URL = reverse("borrowing:borrowing-list")


def detail_url(borrowing_id: int):
    return reverse("borrowing:borrowing-detail", args=[borrowing_id])


def return_url(borrowing_id: int):
    return reverse("borrowing:borrowing-return-borrowing", args=[borrowing_id])


def sample_user(**params):
    unique_id = uuid.uuid4()
    defaults = {
        "email": f"test{unique_id}@test.com",
        "username": f"tester{unique_id}",
        "password": "password"
    }
    defaults.update(params)
    return get_user_model().objects.create_user(**defaults)


def sample_borrowing(user=None, **params):
    book = sample_book()
    if user is None:
        user = sample_user()
    defaults = {
        "borrow_date": "2025-01-02",
        "expected_return_date": "2025-01-14",
        "book_id": book,
        "user_id": user,
    }
    defaults.update(params)
    borrowing = Borrowing.objects.create(**defaults)
    return borrowing


class UnauthenticatedBorrowingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "testuser@test.com",
            "password",
        )
        self.client.force_authenticate(self.user)

    def test_list_borrowing(self):
        book1 = sample_book()
        book2 = sample_book()
        borrowing1 = Borrowing.objects.create(
            borrow_date="2025-01-02",
            expected_return_date="2025-01-14",
            book_id=book1,
            user_id=self.user
        )
        borrowing2 = Borrowing.objects.create(
            borrow_date="2025-01-02",
            expected_return_date="2025-01-14",
            book_id=book2,
            user_id=self.user
        )
        self.assertIsNotNone(borrowing1.id)
        self.assertIsNotNone(borrowing2.id)

        borrowings_count = Borrowing.objects.count()
        self.assertEqual(borrowings_count, 2)

        res = self.client.get(BORROWING_URL)

        borrowings = Borrowing.objects.filter(user_id=self.user)
        serializer = BorrowingSerializer(borrowings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_borrowing_detail(self):
        borrowing = sample_borrowing(user=self.user)

        url = detail_url(borrowing.id)

        res = self.client.get(url)

        serializer = BorrowingDetailSerializer(borrowing)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_borrowing(self):
        book = sample_book()
        payload = {
            "expected_return_date": "2025-01-14",
            "book_id": book.id,
        }
        res = self.client.post(BORROWING_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        borrowing = Borrowing.objects.get(id=res.data['id'])
        self.assertEqual(borrowing.book_id.id, book.id)
        self.assertEqual(borrowing.user_id.id, self.user.id)
        self.assertEqual(str(borrowing.expected_return_date), "2025-01-14")

    def test_create_borrowing_decrease_book_inventory_by_1(self):
        book = sample_book(inventory=5)  # Створюємо книгу з інвентарем 5
        initial_inventory = book.inventory

        payload = {
            "expected_return_date": "2025-01-14",
            "book_id": book.id,
        }
        res = self.client.post(BORROWING_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        book.refresh_from_db()

        self.assertEqual(book.inventory, initial_inventory - 1)

    def test_filter_borrowings_by_current_user(self):
        other_user = get_user_model().objects.create_user(
            "otheruser@test.com",
            "password"
        )
        book1 = sample_book()
        book2 = sample_book()

        Borrowing.objects.create(
            borrow_date="2025-01-02",
            expected_return_date="2025-01-14",
            book_id=book1,
            user_id=self.user
        )
        Borrowing.objects.create(
            borrow_date="2025-01-02",
            expected_return_date="2025-01-14",
            book_id=book2,
            user_id=other_user
        )

        res = self.client.get(BORROWING_URL)

        borrowings = Borrowing.objects.filter(user_id=self.user)
        serializer = BorrowingSerializer(borrowings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_return_borrowing(self):
        book = sample_book()
        payload = {
            "expected_return_date": "2025-01-14",
            "book_id": book.id,
        }
        res = self.client.post(BORROWING_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        borrowing_id = res.data['id']

        return_ur = f"{BORROWING_URL}{borrowing_id}/return/"
        return_res = self.client.post(return_ur, {}, format="json")

        self.assertEqual(return_res.status_code, status.HTTP_200_OK)

        instance = Borrowing.objects.get(pk=borrowing_id)
        self.assertEqual(instance.actual_return_date, datetime.now().date())


class AdminBorrowingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com",
            "password",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_list_all_borrowings(self):
        user = sample_user()

        sample_borrowing(user_id=user)
        sample_borrowing(user_id=user)
        sample_borrowing(user_id=self.user)

        borrowings = Borrowing.objects.all()
        serializer = BorrowingSerializer(borrowings, many=True)

        res = self.client.get(BORROWING_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_borrowings_by_user(self):
        user = sample_user()

        borrowing1 = sample_borrowing(user_id=user)
        borrowing2 = sample_borrowing(user_id=user)
        borrowing3 = sample_borrowing(user_id=self.user)

        serializer1 = BorrowingSerializer(borrowing1)
        serializer2 = BorrowingSerializer(borrowing2)
        serializer3 = BorrowingSerializer(borrowing3)

        res = self.client.get(BORROWING_URL, {"user_id": user.id})

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
