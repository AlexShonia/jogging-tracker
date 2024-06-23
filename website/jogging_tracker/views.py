from rest_framework import viewsets, permissions
from jogging_tracker.models import Jog, User
from jogging_tracker.serializers import JogSerializer, UserSerializer
from .permissions import IsOwnerOrAdmin, IsManagerOrAdmin
import python_weather


class JogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = JogSerializer

    def perform_create(self, serializer):
        # self.getweather()
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Jog.objects.all()
        else:
            return Jog.objects.filter(user=self.request.user)

    async def getweather(self):
        # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
        with python_weather.Client() as client:
            # fetch a weather forecast from a city
            weather = await client.get("New York")

            # returns the current day's forecast temperature (int)
            print(weather.temperature)
            print("something bruh")

            # get the weather forecast for a few days
            for daily in weather.daily_forecasts:
                print(daily)

            # hourly forecasts
            for hourly in daily.hourly_forecasts:
                print(f" --> {hourly!r}")


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.all()
