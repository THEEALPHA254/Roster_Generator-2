# rosters/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemberViewSet, RoleViewSet, RosterViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'members', MemberViewSet, basename='member')  # Specify basename
router.register(r'roles', RoleViewSet, basename='role')  # Specify basename if necessary
router.register(r'rosters', RosterViewSet, basename='roster')  # Specify basename if necessary

# Define the URL patterns for your API
urlpatterns = [
    path('api/', include(router.urls)),
]
