"""
Definition of views.
"""

from app.models import Parking
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from app.serializers import ParkingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class ParkingViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    def get(self, request):
        parks = Parking.objects.all()
        serializer = ParkingSerializer(parks, many=True)
        return Response({"cameras": serializer.data})

