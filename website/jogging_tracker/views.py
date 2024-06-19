from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.request import Request
from jogging_tracker.models import Jog
from jogging_tracker.serializers import JogSerializer
from .permissions import IsOwner


class JogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = JogSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Jog.objects.filter(user=self.request.user)
