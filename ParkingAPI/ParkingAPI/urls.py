"""
Definition of urls for ParkingAPI.
"""

from django.urls import include, path
from rest_framework import routers
from app import views
import app
from django.contrib import admin

#router = routers.DefaultRouter()
#router.register(r'parking', views.ParkingViewSet.as_view())

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/v1/', include('app.urls')),
    path('api/v1/', include('UserValidation.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]