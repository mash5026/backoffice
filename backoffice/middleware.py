# import datetime
# from django.conf import settings
# from django.http import HttpResponse

# class LMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
        
#         if datetime.datetime.now() > settings.L_DATE:
#             return HttpResponse("Please contact support.", status=403)
#         return self.get_response(request)

import json
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser
from backoffice.models import Profile, CustomUser
from django.utils.functional import SimpleLazyObject


LPATH = "D:/backoffice/.venv/Scripts/l_info.json"

class LMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            
            with open(LPATH, "r") as file:
                data = json.load(file)
                datee = datetime.fromisoformat(data["Ldate"])

            # Check if the current date is past the expiration date
            if datetime.now() > datee:
                return HttpResponse("Please contact support.", status=403)
        except (FileNotFoundError, KeyError, ValueError) as e:
            # Handle missing or invalid license file gracefully
            return HttpResponse("information is missing or invalid.", status=403)

        return self.get_response(request)
    

class ProfileToUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and is an instance of Profile
        if isinstance(request.user, Profile):
            # Assign the required properties directly to the request.user
            request.user.is_authenticated = True  # No need to assign to AnonymousUser
            request.user.is_staff = request.user.DJANGO_IS_STAFF
            request.user.is_superuser = request.user.DJANGO_IS_SUPERUSER
        return self.get_response(request)