from django.conf import settings
import requests, time
from datetime import timedelta
from django.urls import reverse
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from jogging_tracker.models import Jog, User
from jogging_tracker.serializers import (
    JogSerializer,
    UserSerializer,
)
from jogging_tracker.permissions import IsOwnerOrAdmin, IsManagerOrAdmin
from django.contrib.auth.hashers import make_password


class JogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = JogSerializer

    def perform_create(self, serializer):
        time = self.request.data["time"]
        weather = self.getweather()
        serializer.save(
            user=self.request.user, time=timedelta(minutes=float(time)), weather=weather
        )

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


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def weekly_report(request):
    current_date = time.strftime("%Y-%m-%d")
    week_ago = time.strftime("%Y-%m-%d", time.localtime(time.time() - 7 * 24 * 60 * 60))
    jogs = Jog.objects.filter(user=request.user, date__range=[week_ago, current_date])

    if jogs.count() == 0:
        return Response("No jogs found in the last week", status.HTTP_404_NOT_FOUND)

    total_km = 0
    total_minutes = 0
    for jog in jogs:
        total_km += jog.distance
        total_minutes += jog.time.total_seconds() / 60

    average_distance = round(total_km / jogs.count(), 1)
    average_speed = round(average_distance / ((total_minutes / jogs.count()) / 60), 1)

    data = {"average_speed": average_speed, "average_distance": average_distance}

    return Response(
        data,
        status=status.HTTP_200_OK,
    )


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
