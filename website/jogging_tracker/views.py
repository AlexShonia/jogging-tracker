import requests, time, datetime
from datetime import timedelta
from django.conf import settings
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from jogging_tracker.models import Jog, User, WeeklyReport
from jogging_tracker.serializers import (
    JogSerializer,
    UserSerializer,
    WeeklyReportSerializer,
    SignUpSerializer,
)
from jogging_tracker.permissions import IsOwnerOrAdmin, IsManagerOrAdmin
from rest_framework_simplejwt.views import TokenObtainPairView
from jogging_tracker.filters import JogFilter


class JogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = JogSerializer
    filterset_class = JogFilter

    def perform_create(self, serializer):
        date_str = self.request.data["date"]
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        days_till_weekend = 6 - date.weekday()
        delta = datetime.timedelta(days=days_till_weekend)
        week_end = date + delta

        if WeeklyReport.objects.filter(
            week_end=week_end, user=self.request.user
        ).exists():
            self.recalculate_weekly_report(
                week_end=week_end, user=self.request.user, adding=self.request.data
            )
        else:
            distance = self.request.data["distance"]
            time = timedelta(minutes=float(self.request.data["time"]))
            average_distance = distance
            average_speed = int(distance) / (time.total_seconds() / 3600)
            WeeklyReport.objects.create(
                user=self.request.user,
                week_end=week_end,
                average_speed=average_speed,
                average_distance=average_distance,
            )

        time = self.request.data["time"]
        weather = self.getweather()

        serializer.save(
            user=self.request.user,
            time=timedelta(minutes=float(time)),
            weather=weather,
        )

    def perform_destroy(self, instance):
        date = instance.date
        days_till_weekend = 6 - date.weekday()
        delta = datetime.timedelta(days=days_till_weekend)
        week_end = date + delta

        jogs = Jog.objects.filter(
            user=self.request.user, date__range=[week_end - timedelta(days=6), week_end]
        )
        if jogs.count() == 1:
            WeeklyReport.objects.filter(
                week_end=week_end, user=self.request.user
            ).delete()
            instance.delete()
        else:
            instance.delete()
            self.recalculate_weekly_report(week_end=week_end, user=self.request.user)

    def recalculate_weekly_report(self, week_end, user, adding=None):
        weekly_report = WeeklyReport.objects.get(user=user, week_end=week_end)

        jogs = Jog.objects.filter(
            user=self.request.user, date__range=[week_end - timedelta(days=6), week_end]
        )

        total_km = 0
        total_minutes = 0
        jog_count = 0
        for jog in jogs:
            jog_count += 1
            total_km += jog.distance
            total_minutes += jog.time.total_seconds() / 60

        if adding:
            jog_count += 1
            total_km += float(adding["distance"])
            total_minutes += float(adding["time"])

        average_distance = round(total_km / jog_count, 1)
        average_speed = round(average_distance / (total_minutes / jog_count / 60), 1)

        WeeklyReport.objects.filter(week_end=week_end, user=self.request.user).update(
            average_speed=average_speed,
            average_distance=average_distance,
        )
        return weekly_report

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Jog.objects.all()
        else:
            return Jog.objects.filter(user=self.request.user)

    def getweather(self):
        api_key = settings.WEATHER_API_KEY

        date = self.request.data["date"]
        city_name = self.request.data["location"]

        if not date or not city_name:
            raise ValidationError("Missing required fields: date or location")

        try:
            timestamp = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        except ValueError:
            raise ValidationError("Invalid date format")

        base_url = settings.WEATHER_URL
        geo_url = f"{base_url}/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)
        geo = geo_response.json()

        if len(geo) == 0:
            raise ValidationError("City not found")

        lat = geo[0].get("lat")
        lon = geo[0].get("lon")

        weather_url = f"{base_url}/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&units=metric&appid={api_key}"
        weather_response = requests.get(weather_url)
        weather_json = weather_response.json()

        if not weather_json["data"]:
            raise ValidationError("Something went wrong")

        temperature = int(weather_json["data"][0]["temp"])
        weather_description = weather_json["data"][0]["weather"][0]["description"]

        return f"{weather_description}, {temperature} degrees"


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class WeeklyReportList(generics.ListAPIView):
    serializer_class = WeeklyReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "admin":
            return WeeklyReport.objects.all()
        else:
            return WeeklyReport.objects.filter(user=self.request.user)


class Register(generics.CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = SignUpSerializer

    def perform_create(self, serializer):
        serializer.save()

        credentials = {
            "email": serializer.validated_data["email"],
            "password": serializer.validated_data["password"],
        }

        token_view = TokenObtainPairView.as_view()
        token_response = token_view(self.request._request, credentials)

        if token_response.status_code == status.HTTP_200_OK:
            self.token_data = token_response.data
        else:
            self.token_data = {"detail": "Token generation failed."}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"token": self.token_data},
            status=status.HTTP_201_CREATED,
        )
