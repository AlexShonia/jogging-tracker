from datetime import timedelta
from django.db.models import Q
from django_filters import FilterSet
from django_filters import DateTimeFilter, NumberFilter, CharFilter
from jogging_tracker.models import Jog, WeeklyReport


class JogFilter(FilterSet):
    from_date = DateTimeFilter(field_name="date", lookup_expr="gt")
    to_date = DateTimeFilter(field_name="date", lookup_expr="lt")
    not_date = DateTimeFilter(field_name="date", exclude=True)
    date_or_filter = CharFilter(method="filter_date_or", field_name="date or filter")

    min_distance = NumberFilter(field_name="distance", lookup_expr="gt")
    max_distance = NumberFilter(field_name="distance", lookup_expr="lt")
    not_distance = NumberFilter(field_name="distance", exclude=True)
    distance_or_filter = CharFilter(
        method="filter_distance_or", field_name="distance or filter"
    )

    min_time = NumberFilter(field_name="time", lookup_expr="gt")
    max_time = NumberFilter(field_name="time", lookup_expr="lt")
    not_time = NumberFilter(field_name="time", exclude=True)
    time_or_filter = CharFilter(method="filter_time_or", field_name="time or filter")

    class Meta:
        model = Jog
        fields = [
            "date",
            "distance",
            "time",
            "location",
            "weather",
        ]

    def filter_date_or(self, queryset, name, value):
        greater_val, lower_val = value.split(",")
        return queryset.filter(Q(date__gt=greater_val) | Q(date__lt=lower_val))

    def filter_distance_or(self, queryset, name, value):
        greater_val, lower_val = value.split(",")
        return queryset.filter(
            Q(distance__gt=greater_val) | Q(distance__lt=lower_val)
        )

    def filter_time_or(self, queryset, name, value):
        greater_val, lower_val = value.split(",")
        return queryset.filter(
            Q(time__gt=timedelta(minutes=greater_val))
            | Q(time__lt=timedelta(minutes=lower_val))
        )

class WeeklyReportFilter(FilterSet):
    from_date = DateTimeFilter(field_name="week_end", lookup_expr="gt")
    to_date = DateTimeFilter(field_name="week_end", lookup_expr="lt")
    not_date = DateTimeFilter(field_name="week_end", exclude=True)
    date_or_filter = CharFilter(method="filter_date_or", field_name="week_end or filter")

    from_avg_distance = NumberFilter(field_name="average_distance", lookup_expr="gt")
    to_avg_distance = NumberFilter(field_name="average_distance", lookup_expr="lt")
    not_avg_distance = NumberFilter(field_name="average_distance", exclude=True)
    avg_distance_or_filter = CharFilter(
        method="filter_avg_distance_or", field_name="average_distance or filter"
    )

    from_avg_speed = NumberFilter(field_name="average_speed", lookup_expr="gt")
    to_avg_speed = NumberFilter(field_name="average_speed", lookup_expr="lt")
    not_avg_speed = NumberFilter(field_name="average_speed", exclude=True)
    avg_speed_or_filter = CharFilter(
        method="filter_avg_speed_or", field_name="average_speed or filter"
    )

    class Meta:
        model = WeeklyReport
        fields = [
            "week_end",
            "average_speed",
            "average_distance",
        ]

    def filter_date_or(self, queryset, name, value):
        greater_val, lower_val = value.split(",")
        return queryset.filter(Q(week_end__gt=greater_val) | Q(week_end__lt=lower_val))

    def filter_avg_distance_or(self, queryset, name, value):
        greater_val, lower_val = value.split(",")
        return queryset.filter(Q(average_distance__gt=greater_val) | Q(average_distance__lt=lower_val))

    def filter_avg_speed_or(self, queryset, name, value):
        greater_val, lower_val = value.split(",")
        return queryset.filter(Q(average_speed__gt=greater_val) | Q(average_speed__lt=lower_val))
