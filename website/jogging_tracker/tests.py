from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class RegisterTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("jogging_tracker:register")
        self.user_list_url = reverse("jogging_tracker:user-list")
        self.jog_list_url = reverse("jogging_tracker:jog-list")
        self.test_email = "test@mail.com"
        self.test_password = "test"

        response = self.client.post(
            self.register_url,
            {
                "email": self.test_email,
                "password": self.test_password,
                "repeat_password": self.test_password,
            },
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.data["token"]["access"]
        )
        self.assertEqual(response.status_code, 201)

    def test_jog_list(self):
        response = self.client.get(self.jog_list_url)

        self.assertEqual(response.status_code, 200)

    def test_users_list(self):
        response = self.client.get(self.user_list_url)

        self.assertEqual(response.status_code, 403)

    def test_add_jog(self):
        response = self.client.post(
            self.jog_list_url,
            {
                "date": "2024-01-01",
                "distance": 1.0,
                "time": 1.0,
                "location": "tbilisi",
            },
        )
        self.assertEqual(response.status_code, 201)


        list_response = self.client.get(self.jog_list_url)
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(
            list_response.content,
            b'{"count":1,"next":null,"previous":null,"results":[{"id":1,"user":"test@mail.com","date":"2024-01-01","distance":1.0,"time":"00:01:00","location":"tbilisi","weather":"clear sky, 4 degrees"}]}',
        )
