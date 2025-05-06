from datetime import timedelta, date
from jogging_tracker.models import WeeklyReport, Jog
from django.db.models import Sum


def calculate_all_weekly_reports():
    week_end = date.today() - timedelta(days=1)
    jogs = Jog.objects.filter(user__reports__week_end = week_end, date__range=[week_end - timedelta(days=6), week_end])

    agg = (
        jogs 
        .values("user_id")
        .annotate(total_km=Sum("distance"), total_time=Sum("time"))
    )

    jog_count = jogs.count()
    for user_agg in agg:
        average_distance = round(user_agg.get("total_km") / jog_count, 1)
        total_minutes = user_agg.get("total_time").total_seconds() / 60
        average_speed = round(average_distance / (total_minutes / jog_count / 60), 1)

        WeeklyReport.objects.filter(week_end=week_end, user=user_agg.get("user_id")).update(
            average_speed=average_speed,
            average_distance=average_distance,
        )
