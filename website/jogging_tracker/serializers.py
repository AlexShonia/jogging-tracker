import datetime
from rest_framework import serializers
from jogging_tracker.models import Jog, User, WeeklyReport, Weather


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = "__all__"


class JogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")
    weather = WeatherSerializer(read_only=True)

    class Meta:
        model = Jog
        fields = [
            "id",
            "user",
            "date",
            "distance",
            "time",
            "location",
            "weather",
        ]

    def validate_date(self, value):
        today = datetime.date.today()
        delta = datetime.timedelta(days=today.weekday() + 1)
        last_week_end = today - delta

        if value < last_week_end:
            raise serializers.ValidationError(
                "Date must be in this week"
            )

        if value > today:
            raise serializers.ValidationError(
                "Date must be not be in the future"
            )

        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "role"]


class WeeklyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyReport
        fields = [
            "user",
            "week_end",
            "average_distance",
            "average_speed",
        ]


class SignUpSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "repeat_password"]

    def validate_repeat_password(self, value):
        data = self.get_initial()
        password = data["password"]
        repeat_password = value

        if password != repeat_password:
            raise serializers.ValidationError(
                {"repeat_password": "Passwords do not match."}
            )

        return value

    def save(self, **kwargs):
        self.validated_data.pop("repeat_password")
        return User.objects.create_user(**self.validated_data)
