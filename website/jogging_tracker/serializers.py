from rest_framework import serializers
from jogging_tracker.models import Jog, User


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
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "email"]
