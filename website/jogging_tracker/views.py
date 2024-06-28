import requests, time, datetime
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, permissions, status, mixins, generics
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from jogging_tracker.models import Jog, User, WeeklyReport
from jogging_tracker.serializers import (
    JogSerializer,
    UserSerializer,
    WeeklyReportSerializer,
)
from jogging_tracker.permissions import IsOwnerOrAdmin, IsManagerOrAdmin


class JogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = JogSerializer

    def perform_create(self, serializer):
        date_str = self.request.data["date"]
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        days_till_weekend = 6 - date.weekday()
        delta = datetime.timedelta(days=days_till_weekend)
        week_end = date + delta

        if WeeklyReport.objects.filter(week_end=week_end).exists():
            weekly_report = self.recalculate_weekly_report(
                week_end=week_end, user=self.request.user, adding=self.request.data
            )
        else:
            distance = self.request.data["distance"]
            time = timedelta(minutes=float(self.request.data["time"]))
            average_distance = distance
            average_speed = int(distance) / (time.total_seconds() / 3600)
            weekly_report = WeeklyReport.objects.create(
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
            weekly_report=weekly_report,
        )

    def perform_destroy(self, instance):
        week_end = instance.weekly_report.week_end
        if instance.weekly_report.jogs.count() == 1:
            WeeklyReport.objects.filter(
                week_end=week_end, user=self.request.user
            ).delete()
            instance.delete()
        else:
            instance.delete()
            self.recalculate_weekly_report(week_end=week_end, user=self.request.user)

    def recalculate_weekly_report(self, week_end, user, adding=None):
        weekly_report = WeeklyReport.objects.get(user=user, week_end=week_end)

        jogs = weekly_report.jogs.all()

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
        return WeeklyReport.objects.filter(user=self.request.user)


@api_view(["POST"])
def register(request):
    data = request.data

    try:
        User.objects.create(
            email=data["email"],
            username=data["email"],
            password=make_password(data["password"]),
        )

        return Response("Succesful registration", status=status.HTTP_200_OK)
    except:
        return Response(
            "User with this email exists", status=status.HTTP_400_BAD_REQUEST
        )
