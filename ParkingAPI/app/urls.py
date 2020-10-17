

from django.urls import include, path
from rest_framework import routers
from app import views
from django.contrib import admin

#router = routers.DefaultRouter()
#router.register(r'parking', views.ParkingViewSet.as_view())

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.ParkingViewSet.as_view()),
    path('parkings', views.ParkingViewSet.as_view()),
]