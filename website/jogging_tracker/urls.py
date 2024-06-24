from django.urls import path, include
from rest_framework.routers import SimpleRouter

from jogging_tracker import views

router = SimpleRouter()
router.register(r"jogs", views.JogViewSet, basename="jog")
router.register(r"users", views.UserViewSet, basename="user")
urlpatterns = [
    path("", views.index_view, name="index"),
    path("weekly_report/", views.weekly_report, name="weekly_report"),
]

urlpatterns += router.urls
