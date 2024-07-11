from rest_framework import serializers
from jogging_tracker.models import Jog, User, WeeklyReport


class JogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")

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
        read_only_field = "weather"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


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

    def save(self, **kwargs):
        repeat_password = self.validated_data.pop("repeat_password")
        password = self.validated_data.get("password")

        if password != repeat_password:
            raise serializers.ValidationError(
                {"repeat_password": "Passwords do not match."}
            )

        return User.objects.create_user(**self.validated_data)
