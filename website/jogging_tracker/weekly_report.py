from datetime import timedelta, date
from jogging_tracker.models import WeeklyReport, Jog
from time import sleep

def recalculate_weekly_report(week_end, user, adding=False):

    # simulate expensive computation
    sleep(5)

    week_end = date.fromisoformat(week_end)
    weekly_report = WeeklyReport.objects.get(user=user, week_end=week_end)

    jogs = Jog.objects.filter(
        user=user, date__range=[week_end - timedelta(days=6), week_end]
    )

    total_km = 0
    total_minutes = 0
    jog_count = 0
    for jog in jogs:
        jog_count += 1
        total_km += jog.distance
        total_minutes += jog.time.total_seconds() / 60

    if adding:
        jog_count += 1
        total_km += adding.get("distance")
        total_minutes += adding.get("total_minutes")

    average_distance = round(total_km / jog_count, 1)
    average_speed = round(average_distance / (total_minutes / jog_count / 60), 1)

    WeeklyReport.objects.filter(week_end=week_end, user=user).update(
        average_speed=average_speed,
        average_distance=average_distance,
    )
    return weekly_report