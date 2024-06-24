from rest_framework import viewsets, permissions
from jogging_tracker.models import Jog, User
from jogging_tracker.serializers import JogSerializer, UserSerializer
from .permissions import IsOwnerOrAdmin, IsManagerOrAdmin
import requests, time
from dotenv import load_dotenv
import os
from rest_framework.exceptions import ValidationError


class JogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = JogSerializer

    def perform_create(self, serializer):
        weather = self.getweather()
        serializer.save(user=self.request.user)
        serializer.save(weather=weather)

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Jog.objects.all()
        else:
            return Jog.objects.filter(user=self.request.user)

    def getweather(self):
        load_dotenv()
        api_key = os.environ.get("WEATHER_API_KEY")

        date = self.request.data["date"]
        city_name = self.request.data["location"]

        if not date or not city_name:
            raise ValidationError("Missing required fields: date or location")

        try:
            timestamp = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        except ValueError:
            raise ValidationError("Invalid date format")

        geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)
        geo = geo_response.json()

        if len(geo) == 0:
            raise ValidationError("City not found")

        lat = geo[0].get("lat")
        lon = geo[0].get("lon")

        weather_url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&units=metric&appid={api_key}"
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
