from django.urls import path, include
from rest_framework.routers import DefaultRouter

from jogging_tracker import views

router = DefaultRouter()
router.register(r"jogs", views.JogViewSet, basename="jog")
router.register(r"users", views.UserViewSet, basename="user")

app_name = "jogging_tracker"
urlpatterns = [
    path("", include(router.urls)),
    path("weekly-report/", views.WeeklyReportList.as_view(), name="weekly_report"),
    path("register/", views.Register.as_view(), name="register"),
]
