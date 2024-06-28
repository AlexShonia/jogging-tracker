from rest_framework import serializers
from jogging_tracker.models import Jog, User, WeeklyReport


class JogSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Jog
        fields = [
            "url",
            "id",
            "user",
            "date",
            "distance",
            "time",
            "location",
            "weather",
        ]
        read_only_field = "weather"


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "email"]


class WeeklyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyReport
        fields = [
            "week_end",
            "average_distance",
            "average_speed",
            "jogs",
        ]
