from datetime import timedelta
from django.db.models import Q
from rest_framework import filters


def custom_jog_filter(queryset, filter_option, value):
    match filter_option:
        case "date":
            return queryset.filter(date=value)
        case "not_date":
            return queryset.exclude(date=value)
        case "from_date":
            return queryset.filter(date__gt=value)
        case "to_date":
            return queryset.filter(date__lt=value)
        case "date_or":
            greater_val, lower_val = value.split(",")
            return queryset.filter(Q(date__gt=greater_val) | Q(date__lt=lower_val))
        case "distance":
            return queryset.filter(distance=value)
        case "not_distance":
            return queryset.exclude(distance=value)
        case "from_distance":
            return queryset.filter(distance__gt=value)
        case "to_distance":
            return queryset.filter(distance__lt=value)
        case "distance_or":
            greater_val, lower_val = value.split(",")
            return queryset.filter(
                Q(distance__gt=greater_val) | Q(distance__lt=lower_val)
            )
        case "time":
            return queryset.filter(time=timedelta(minutes=int(value)))
        case "not_time":
            return queryset.exclude(time=timedelta(minutes=int(value)))
        case "from_time":
            return queryset.filter(time__gt=timedelta(minutes=int(value)))
        case "to_time":
            return queryset.filter(time__lt=timedelta(minutes=int(value)))
        case "time_or":
            greater_val, lower_val = value.split(",")
            return queryset.filter(
                Q(time__gt=timedelta(minutes=int(greater_val)))
                | Q(time__lt=timedelta(minutes=int(lower_val)))
            )
        case "location":
            return queryset.filter(location=value)
        case "not_location":
            return queryset.exclude(location=value)

    return queryset


class JogFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_options = [
            "date",
            "not_date",
            "from_date",
            "to_date",
            "date_or",
            "distance",
            "not_distance",
            "from_distance",
            "to_distance",
            "distance_or",
            "time",
            "not_time",
            "from_time",
            "to_time",
            "time_or",
            "location",
            "not_location",
        ]

        if len(request.query_params) == 0:
            return queryset
        else:
            for filter_option in request.query_params:
                if filter_option not in filter_options:
                    continue
                value = request.query_params.get(filter_option)
                queryset = custom_jog_filter(queryset, filter_option, value)
            return queryset


def custom_weekly_report_filter(queryset, filter_option, value):
    match filter_option:
        case "date":
            return queryset.filter(week_end=value)
        case "not_date":
            return queryset.exclude(week_end=value)
        case "from_date":
            return queryset.filter(week_end__gt=value)
        case "to_date":
            return queryset.filter(week_end__lt=value)
        case "date_or":
            greater_val, lower_val = value.split(",")
            return queryset.filter(
                Q(week_end__gt=greater_val) | Q(week_end__lt=lower_val)
            )
        case "average_speed":
            return queryset.filter(average_speed=value)
        case "not_average_speed":
            return queryset.exclude(average_speed=value)
        case "from_average_speed":
            return queryset.filter(average_speed__gt=value)
        case "to_average_speed":
            return queryset.filter(average_speed__lt=value)
        case "average_speed_or":
            greater_val, lower_val = value.split(",")
            return queryset.filter(
                Q(average_speed__gt=greater_val) | Q(average_speed__lt=lower_val)
            )
        case "average_distance":
            return queryset.filter(average_distance=value)
        case "not_average_distance":
            return queryset.exclude(average_distance=value)
        case "from_average_distance":
            return queryset.filter(average_distance__gt=value)
        case "to_average_distance":
            return queryset.filter(average_distance__lt=value)
        case "average_distance_or":
            greater_val, lower_val = value.split(",")
            return queryset.filter(
                Q(average_distance__gt=greater_val) | Q(average_distance__lt=lower_val)
            )


class WeeklyReportFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_options = [
            "date",
            "not_date",
            "from_date",
            "to_date",
            "date_or",
            "average_speed",
            "not_average_speed",
            "from_average_speed",
            "to_average_speed",
            "average_speed_or",
            "average_distance",
            "not_average_distance",
            "from_average_distance",
            "to_average_distance",
            "average_distance_or",
        ]

        if len(request.query_params) == 0:
            return queryset
        else:
            for filter_option in request.query_params:
                if filter_option not in filter_options:
                    continue
                value = request.query_params.get(filter_option)
                queryset = custom_weekly_report_filter(queryset, filter_option, value)
            return queryset
