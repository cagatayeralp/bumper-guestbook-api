from django.urls import reverse
from rest_framework.test import APITestCase


TEST_USER = "cagatay_1"


class UserStatsAPITest(APITestCase):
    def test_user_stats_single_user(self):
        for i in range(3):
            self.client.post(
                reverse("entry-create"),
                {
                    "name": TEST_USER,
                    "subject": f"subject_{i}",
                    "message": f"message_{i}",
                },
                format="json",
            )

        response = self.client.get(reverse("user-stats"))

        self.assertEqual(response.status_code, 200)

        users = response.data["users"]

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["username"], TEST_USER)
        self.assertEqual(users[0]["total_messages"], 3)
        self.assertEqual(users[0]["last_entry"], "subject_2 | message_2")

    def test_user_stats_multiple_users(self):
        self.client.post(
            reverse("entry-create"),
            {
                "name": "cagatay_1",
                "subject": "s1",
                "message": "m1",
            },
            format="json",
        )
        self.client.post(
            reverse("entry-create"),
            {
                "name": "cagatay_2",
                "subject": "s2",
                "message": "m2",
            },
            format="json",
        )

        response = self.client.get(reverse("user-stats"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["users"]), 2)

    def test_user_stats_latest_entry(self):
        self.client.post(
            reverse("entry-create"),
            {
                "name": TEST_USER,
                "subject": "old",
                "message": "old",
            },
            format="json",
        )
        self.client.post(
            reverse("entry-create"),
            {
                "name": TEST_USER,
                "subject": "new",
                "message": "new",
            },
            format="json",
        )

        response = self.client.get(reverse("user-stats"))

        user = response.data["users"][0]

        self.assertEqual(user["total_messages"], 2)
        self.assertEqual(user["last_entry"], "new | new")
