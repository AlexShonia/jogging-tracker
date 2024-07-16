from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from jogging_tracker.models import User, WeeklyReport


class RegisterTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("jogging_tracker:register")
        self.login_url = reverse("token_obtain_pair")
        self.user_list_url = reverse("jogging_tracker:user-list")
        self.jog_list_url = reverse("jogging_tracker:jog-list")
        self.weekly_report_url = reverse("jogging_tracker:weekly_report")
        self.test_email = "test@mail.com"
        self.test_password = "test"
        self.admin_email = "admin@mail.com"
        self.admin_password = "admin"

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

        superuser = User.objects.create_superuser(
            email=self.admin_email, password=self.admin_password
        )
        self.assertEqual(superuser.role, "admin")

    def test_jog_list(self):
        response = self.client.get(self.jog_list_url)

        self.assertEqual(response.status_code, 200)

    def test_admin_permissions(self):
        add_jog_response = self.client.post(
            self.jog_list_url,
            {
                "date": "2024-01-01",
                "distance": 1.0,
                "time": 1.0,
                "location": "tbilisi",
            },
        )

        self.assertEqual(add_jog_response.status_code, 201)

        response = self.client.get(self.user_list_url)

        self.assertEqual(response.status_code, 403)

        login_response = self.client.post(
            self.login_url, {"email": self.admin_email, "password": self.admin_password}
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + login_response.data["access"]
        )

        # User permissions
        User.objects.create_user(email="test1@mail.com", password="test1")

        user_list_response = self.client.get(self.user_list_url)

        self.assertEqual(user_list_response.status_code, 200)
        self.assertEqual(
            user_list_response.content,
            b'{"count":3,"next":null,"previous":null,"results":[{"id":3,"email":"test@mail.com","role":"customer"},{"id":4,"email":"admin@mail.com","role":"admin"},{"id":5,"email":"test1@mail.com","role":"customer"}]}',
        )

        update_user_response = self.client.put(
            reverse("jogging_tracker:user-detail", args=[3]),
            {"email": self.test_email, "role": "manager"},
        )

        self.assertEqual(update_user_response.status_code, 200)
        self.assertEqual(
            update_user_response.content,
            b'{"id":3,"email":"test@mail.com","role":"manager"}',
        )

        delete_user_response = self.client.delete(
            reverse("jogging_tracker:user-detail", args=[5])
        )
        self.assertEqual(delete_user_response.status_code, 204)

        # Jog permissions
        jog_list_response = self.client.get(self.jog_list_url)

        self.assertEqual(jog_list_response.status_code, 200)
        self.assertEqual(
            jog_list_response.content,
            b'{"count":1,"next":null,"previous":null,"results":[{"id":2,"user":"test@mail.com","date":"2024-01-01","distance":1.0,"time":"00:01:00","location":"tbilisi","weather":{"id":2,"temperature":4,"description":"clear sky"}}]}',
        )

        update_jog_response = self.client.put(
            reverse("jogging_tracker:jog-detail", args=[2]),
            {
                "date": "2024-01-01",
                "distance": 2.0,
                "time": 1.0,
                "location": "tbilisi",
            },
        )

        self.assertEqual(update_jog_response.status_code, 200)
        self.assertEqual(
            update_jog_response.content,
            b'{"id":2,"user":"test@mail.com","date":"2024-01-01","distance":2.0,"time":"00:00:01","location":"tbilisi","weather":{"id":2,"temperature":4,"description":"clear sky"}}',
        )

        delete_jog_response = self.client.delete(
            reverse("jogging_tracker:jog-detail", args=[2])
        )
        self.assertEqual(delete_jog_response.status_code, 204)

        weekly_report_response = self.client.get(self.weekly_report_url)

        self.assertEqual(weekly_report_response.status_code, 200)
        self.assertEqual(
            weekly_report_response.content,
            b'{"count":0,"next":null,"previous":null,"results":[]}',
        )

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
            b'{"count":1,"next":null,"previous":null,"results":[{"id":1,"user":"test@mail.com","date":"2024-01-01","distance":1.0,"time":"00:01:00","location":"tbilisi","weather":{"id":1,"temperature":4,"description":"clear sky"}}]}',
        )
