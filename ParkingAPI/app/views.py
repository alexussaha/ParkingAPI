"""
Definition of views.
"""

from app.models import Parking
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from app.serializers import ParkingSerializer


class ParkingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = [permissions.IsAuthenticated]


