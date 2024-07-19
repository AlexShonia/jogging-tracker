from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from jogging_tracker.models import User, WeeklyReport


class Test(TestCase):
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
        self.manager_email = "manager@mail.com"
        self.manager_password = "manager"

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

        manager = User.objects.create_user(
            email=self.manager_email, password=self.manager_password
        )
        manager.role = "manager"
        manager.save()
        self.assertEqual(manager.role, "manager")

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
        user_list_json = user_list_response.json()
        self.assertEqual(user_list_response.status_code, 200)
        self.assertEqual(user_list_json["count"], 4)

        test1_user = User.objects.get(email="test1@mail.com")
        update_user_response = self.client.put(
            reverse("jogging_tracker:user-detail", args=[test1_user.id]),
            {"email": "test1@mail.com", "role": "manager"},
        )
        update_user_json = update_user_response.json()
        self.assertEqual(update_user_response.status_code, 200)
        self.assertEqual(update_user_json["role"], "manager")

        delete_user_response = self.client.delete(
            reverse("jogging_tracker:user-detail", args=[test1_user.id])
        )
        self.assertEqual(delete_user_response.status_code, 204)

        # Jog permissions
        jog_list_response = self.client.get(self.jog_list_url)
        jog_list_json = jog_list_response.json()
        self.assertEqual(jog_list_response.status_code, 200)
        self.assertEqual(jog_list_json["count"], 1)

        for jog in jog_list_json["results"]:
            if jog["date"] == "2024-01-01":
                jog_id = jog["id"]

        update_jog_response = self.client.put(
            reverse("jogging_tracker:jog-detail", args=[jog_id]),
            {
                "date": "2024-01-01",
                "distance": 2.0,
                "time": 1.0,
                "location": "tbilisi",
            },
        )
        update_jog_json = update_jog_response.json()
        self.assertEqual(update_jog_response.status_code, 200)
        self.assertEqual(update_jog_json["distance"], 2.0)

        delete_jog_response = self.client.delete(
            reverse("jogging_tracker:jog-detail", args=[jog_id])
        )
        self.assertEqual(delete_jog_response.status_code, 204)

        # Weekly report permissions
        weekly_report_response = self.client.get(self.weekly_report_url)
        weekly_report_json = weekly_report_response.json()
        self.assertEqual(weekly_report_response.status_code, 200)
        self.assertEqual(weekly_report_json["count"], 0)

    def test_manager_permissions(self):
        add_jog_response = self.client.post(
            self.jog_list_url,
            {
                "date": "2024-01-01",
                "distance": 1.0,
                "time": 1.0,
                "location": "tbilisi",
            },
        )

        login_response = self.client.post(
            self.login_url,
            {"email": self.manager_email, "password": self.manager_password},
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + login_response.data["access"]
        )

        # Jog permissions
        jog_list_response = self.client.get(self.jog_list_url)
        jog_list_json = jog_list_response.json()
        self.assertEqual(jog_list_response.status_code, 200)
        self.assertEqual(jog_list_json["count"], 0)

        # User permissions
        User.objects.create_user(email="test1@mail.com", password="test1")

        user_list_response = self.client.get(self.user_list_url)
        user_list_json = user_list_response.json()
        self.assertEqual(user_list_response.status_code, 200)
        self.assertEqual(user_list_json["count"], 4)

        test1_user = User.objects.get(email="test1@mail.com")
        update_user_response = self.client.put(
            reverse("jogging_tracker:user-detail", args=[test1_user.id]),
            {"email": "test1@mail.com", "role": "manager"},
        )
        update_user_json = update_user_response.json()
        self.assertEqual(update_user_response.status_code, 200)
        self.assertEqual(update_user_json["role"], "manager")

        delete_user_response = self.client.delete(
            reverse("jogging_tracker:user-detail", args=[test1_user.id])
        )
        self.assertEqual(delete_user_response.status_code, 204)

        # Weekly report permissions
        weekly_report_response = self.client.get(self.weekly_report_url)
        weekly_report_json = weekly_report_response.json()
        self.assertEqual(weekly_report_response.status_code, 200)
        self.assertEqual(weekly_report_json["count"], 0)

    def test_customer_permissions(self):
        jog_list_response = self.client.get(self.jog_list_url)
        jog_list_json = jog_list_response.json()
        self.assertEqual(jog_list_response.status_code, 200)
        self.assertEqual(jog_list_json["count"], 0)

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

        jog_list_response = self.client.get(self.jog_list_url)
        jog_list_json = jog_list_response.json()

        for jog in jog_list_json["results"]:
            if jog["date"] == "2024-01-01":
                jog_id = jog["id"]

        update_jog_response = self.client.put(
            reverse("jogging_tracker:jog-detail", args=[jog_id]),
            {
                "date": "2024-01-01",
                "distance": 2.0,
                "time": 1.0,
                "location": "tbilisi",
            },
        )
        update_jog_json = update_jog_response.json()
        self.assertEqual(update_jog_json["distance"], 2.0)

        weekly_report_response = self.client.get(self.weekly_report_url)
        weekly_report_json = weekly_report_response.json()
        self.assertEqual(weekly_report_response.status_code, 200)
        self.assertEqual(weekly_report_json["count"], 1)
        self.assertEqual(weekly_report_json["results"][0]["week_end"], "2024-01-07")
        self.assertEqual(weekly_report_json["results"][0]["average_distance"], 1.0)
        self.assertEqual(weekly_report_json["results"][0]["average_speed"], 3600.0)

