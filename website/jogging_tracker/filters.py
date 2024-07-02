from django.db.models import Q
from django_filters import FilterSet
from django_filters import DateTimeFilter, NumberFilter, CharFilter
from jogging_tracker.models import Jog


class JogFilter(FilterSet):
    from_date = DateTimeFilter(field_name="date", lookup_expr="gt")
    to_date = DateTimeFilter(field_name="date", lookup_expr="lt")
    not_date = DateTimeFilter(field_name="date", exclude=True)

    min_distance = NumberFilter(field_name="distance", lookup_expr="gt")
    max_distance = NumberFilter(field_name="distance", lookup_expr="lt")
    not_distance = NumberFilter(field_name="distance", exclude=True)

    min_time = NumberFilter(field_name="time", lookup_expr="gt")
    max_time = NumberFilter(field_name="time", lookup_expr="lt")
    not_time = NumberFilter(field_name="time", exclude=True)

    distance_or_filter = CharFilter(method="filter_distance_or", field_name="distance or filter")

    class Meta:
        model = Jog
        fields = [
            "date",
            "distance",
            "time",
            "location",
            "weather",
        ]

    def filter_distance_or(self, queryset, name, value):
        greater_val, lower_val = value.split(",")
        return queryset.filter(Q(distance__gt=float(greater_val)) | Q(distance__lt=float(lower_val)))
