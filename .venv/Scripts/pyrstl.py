# import datetime
# from django.conf import settings
# from django.core.management.base import BaseCommand

# class Command(BaseCommand):
#     help = 'Reset'

#     def add_arguments(self, parser):
#         parser.add_argument('secret_key', type=str, help='Secret key to reset the license')

#     def handle(self, *args, **kwargs):
#         secret_key = kwargs['secret_key']
#         correct_key = "MmtT@#123321@#$%110"

#         if secret_key == correct_key:
#             new_expiration_date = datetime.datetime.now() + datetime.timedelta(days=90)
#             settings.L_DATE = new_expiration_date
#             self.stdout.write(self.style.SUCCESS('Renewed it again.'))
#         else:
#             self.stdout.write(self.style.ERROR('Invalid secret key'))

import os
import json
from datetime import datetime, timedelta

# Define the path to the JSON file
LPATH = "D:/backoffice/.venv/Scripts/l_info.json"  # Update with the actual path


# Retrieve the secret key from the environment variable
correct_key = "MmtT@#123321@#$%110"
input_key = input("Enter the activation key: ")

if input_key == correct_key:
    # Read the current license data
    with open(LPATH, "r") as file:
        license_data = json.load(file)

    # Update the expiration date to 3 months from now
    new_expiration_date = datetime.now() + timedelta(days=90)
    license_data["Ldate"] = new_expiration_date.isoformat()

    # Write the updated data back to the file
    with open(LPATH, "w") as file:
        json.dump(license_data, file)

    print("License renewed for 3 more months.")
else:
    print("Invalid secret key.")