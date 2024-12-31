from django.http import JsonResponse
from .models import Location
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django import forms
from django.http import JsonResponse
from .models import Profile
from .utils import IsnationalCode
from django.core.exceptions import ValidationError



def get_child_locations(request):
    parent_id = request.GET.get('parent_id')
    if parent_id:
        child_locations = Location.objects.filter(parentid=parent_id)
    else:
        child_locations = Location.objects.none()
    
    locations = [{'id': loc.id, 'name': loc.name} for loc in child_locations]
    return JsonResponse({'locations': locations})


def check_nationalid(request, nationalid):
    # Check if the nationalid already exists in the Profile model
    if len(nationalid) == 11 and nationalid.startswith('9'):
        nationalid = nationalid[1:]
    exists = Profile.objects.filter(NATIONALID=nationalid).exists()
    return JsonResponse({'exists': exists})


def validate_nationalid(request, nationalid):
    # Check if the national ID is valid using the IsnationalCode function
    if len(nationalid) == 11 and nationalid.startswith('9'):
        nationalid = nationalid[1:]
    try:
        if not IsnationalCode(nationalid):
            return JsonResponse({'valid': False})
        return JsonResponse({'valid': True})
    except ValidationError:
        return JsonResponse({'valid': False})