from django.urls import reverse
from rest_framework.test import APITestCase

from guestbook.models import Entry, GuestUser


TEST_USER = "cagatay_1"


class EntryAPITest(APITestCase):
    def test_create_entry_success(self):
        response = self.client.post(
            reverse("entry-create"),
            {
                "name": TEST_USER,
                "subject": "hello",
                "message": "first message",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(GuestUser.objects.count(), 1)
        self.assertEqual(response.data["user"], TEST_USER)

    def test_create_entry_existing_user(self):
        payload = {
            "name": TEST_USER,
            "subject": "hello",
            "message": "first message",
        }

        self.client.post(reverse("entry-create"), payload, format="json")
        self.client.post(reverse("entry-create"), payload, format="json")

        self.assertEqual(GuestUser.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 2)

    def test_create_entry_validation_errors(self):
        response = self.client.post(reverse("entry-create"), {}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.data)
        self.assertIn("subject", response.data)
        self.assertIn("message", response.data)

    def test_create_entry_blank_values(self):
        response = self.client.post(
            reverse("entry-create"),
            {
                "name": " ",
                "subject": " ",
                "message": " ",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_create_entry_trims_values(self):
        response = self.client.post(
            reverse("entry-create"),
            {
                "name": f"  {TEST_USER}  ",
                "subject": "  hello  ",
                "message": "  message  ",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user"], TEST_USER)
        self.assertEqual(response.data["subject"], "hello")
        self.assertEqual(response.data["message"], "message")

    def test_create_entry_message_max_length(self):
        response = self.client.post(
            reverse("entry-create"),
            {
                "name": TEST_USER,
                "subject": "hello",
                "message": "c" * 2001,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.data)
