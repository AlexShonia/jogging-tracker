from celery import shared_task
from jogging_tracker.weekly_report import recalculate_weekly_report

@shared_task()
def recalculate_weekly_report_task(week_end, user, adding=False):
    recalculate_weekly_report(week_end, user, adding)

