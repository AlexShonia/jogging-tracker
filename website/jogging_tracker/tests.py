from django.test import TestCase

# Create your tests here.
import datetime
import time

datetime.date.today()
days_till_weekend = 6 - datetime.date.today().weekday()
delta = datetime.timedelta(days=days_till_weekend)

week_end = datetime.date.today() + delta
week_ago = time.strftime("%Y-%m-%d", time.localtime(time.mktime(week_end.timetuple()) - 7 * 24 * 60 * 60))

adding = 0

if adding:
    print("yes")
