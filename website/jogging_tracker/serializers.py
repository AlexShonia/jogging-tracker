from rest_framework import serializers
from jogging_tracker.models import Jog


class JogSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
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
