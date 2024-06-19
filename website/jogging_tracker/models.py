from django.db import models


class Jog(models.Model):
    date = models.DateField()
    distance = models.FloatField()
    time = models.DurationField()
    location = models.CharField(max_length=100)
    user = models.ForeignKey("auth.User", related_name="jogs", on_delete=models.CASCADE)

    class Meta:
        ordering = ["date"]
