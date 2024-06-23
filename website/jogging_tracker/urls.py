from django.urls import path, include
from rest_framework.routers import DefaultRouter

from jogging_tracker import views

router = DefaultRouter()
router.register(r"jogs", views.JogViewSet, basename="jog")
router.register(r"users", views.UserViewSet, basename="user")
urlpatterns = [path("", include(router.urls))]
