from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email


class Jog(models.Model):
    date = models.DateField()
    distance = models.FloatField()
    time = models.DurationField()
    location = models.CharField(max_length=100)
    weather = models.OneToOneField(
        "jogging_tracker.Weather", on_delete=models.CASCADE, null=True
    )
    user = models.ForeignKey(
        "jogging_tracker.User", related_name="jogs", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["date"]


class Weather(models.Model):
    temperature = models.IntegerField()
    description = models.CharField(max_length=100)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, role, **extra_fields):
        validate_email(email)
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        role = "customer"
        return self._create_user(email, password, role, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        role = "admin"
        return self._create_user(email, password, role, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Role(models.TextChoices):
        Customer = "customer"
        Manager = "manager"
        Admin = "admin"

    role = models.CharField(max_length=255, choices=Role.choices, default=Role.Customer)


class WeeklyReport(models.Model):
    week_end = models.DateField()
    user = models.ForeignKey(
        "jogging_tracker.User", related_name="reports", on_delete=models.CASCADE
    )
    average_speed = models.FloatField()
    average_distance = models.FloatField()
