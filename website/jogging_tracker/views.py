import datetime
from datetime import timedelta
from rest_framework import viewsets, permissions, generics, status, mixins
from rest_framework.response import Response
from jogging_tracker.models import Jog, User, WeeklyReport, Weather
from jogging_tracker.serializers import (
    JogSerializer,
    UserSerializer,
    WeeklyReportSerializer,
    SignUpSerializer,
)
from jogging_tracker.permissions import IsOwnerOrAdmin, IsManagerOrAdmin
from rest_framework_simplejwt.views import TokenObtainPairView
from jogging_tracker.filters import JogFilter, WeeklyReportFilter, JogFilter
from django_filters.rest_framework import DjangoFilterBackend
from jogging_tracker.weather import get_weather

class JogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = JogSerializer
    filter_backends = [JogFilter]

    def perform_create(self, serializer):
        date: datetime.date = serializer.validated_data.get("date")
        days_till_weekend = 6 - date.weekday()
        delta = datetime.timedelta(days=days_till_weekend)
        week_end = date + delta

        if not WeeklyReport.objects.filter(
            week_end=week_end, user=self.request.user
        ).exists():
            distance = serializer.validated_data.get("distance")
            time = serializer.validated_data.get("time")
            average_distance = distance
            average_speed = int(distance) / (time.total_seconds() / 3600)
            WeeklyReport.objects.create(
                user=self.request.user,
                week_end=week_end,
                average_speed=average_speed,
                average_distance=average_distance,
            )

        time = serializer.validated_data.get("time")
        weather_data = get_weather(serializer)
        weather = Weather.objects.create(**weather_data)

        serializer.save(
            user=self.request.user,
            time=time * 60,
            weather=weather,
        )

    def destroy(self,  request, *args, **kwargs):
        instance = self.get_object()
        date: datetime.date = instance.date
        days_till_weekend = 6 - date.weekday()
        delta = datetime.timedelta(days=days_till_weekend)
        week_end = date + delta
        
        if week_end < date.today():
            return Response(data={"message": "Can't delete jog from past weeks"}, status=status.HTTP_400_BAD_REQUEST)

        jogs = Jog.objects.filter(
            user=instance.user, date__range=[week_end - timedelta(days=6), week_end]
        )

        if jogs.count() == 1:
            WeeklyReport.objects.filter(week_end=week_end, user=instance.user).delete()
            instance.delete()
        else:
            instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Jog.objects.all()
        else:
            return Jog.objects.filter(user=self.request.user)


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "email"]


class WeeklyReportList(generics.ListAPIView):
    serializer_class = WeeklyReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [WeeklyReportFilter]

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
