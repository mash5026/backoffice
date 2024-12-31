from django.urls import path
from .views import get_child_locations, check_nationalid, validate_nationalid

urlpatterns = [
    path('get-child-locations/', get_child_locations, name='get_child_locations'),
    path('check-nationalid/<str:nationalid>/', check_nationalid, name='check_nationalid'),
    path('validate-nationalid/<str:nationalid>/', validate_nationalid, name='validate_nationalid'),
]