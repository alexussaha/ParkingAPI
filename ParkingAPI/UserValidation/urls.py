from django.urls import include, path
from rest_framework import routers
from UserValidation import views
import app
from django.contrib import admin

#router = routers.DefaultRouter()
#router.register(r'parking', views.ParkingViewSet.as_view())

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("users/", views.UserCreate.as_view(), name="user_create"),
    path("login/", views.LoginView.as_view(), name="login"),
]
