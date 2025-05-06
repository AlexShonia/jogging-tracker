from celery import shared_task
from jogging_tracker.weekly_report import calculate_all_weekly_reports

@shared_task()
def calculate_all_weekly_reports_task():
    calculate_all_weekly_reports()
