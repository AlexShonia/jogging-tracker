from django.test import TestCase
from django.test import Client
from django.urls import reverse
from rest_framework.test import APIClient


class RegisterTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("jogging_tracker:register")
        self.login_url = reverse("jogging_tracker:login")
        self.test_email = "test@mail.com"
        self.test_password = "test"
    def test_register(self):
        client = APIClient()
        response = client.post(
            reverse("jogging_tracker:register"),
            {"email": "test@mail.com", "password": "test", "repeat_password": "test"},
        )

        self.assertEqual(response.status_code, 201)
        client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["token"]["access"])

        response = client.get(reverse("jogging_tracker:jog-list"))

        print(response.content)



    def test_users_list(self):
        client = APIClient()
        response = client.get(reverse("jogging_tracker:user-list"))
        
        print(response.content)