import os
import django
from django.contrib.auth.models import User
from django.db import connections, transaction

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # Replace 'myproject' with your actual project name
django.setup()

def create_superuser(username, password, using='database2'):
    try:
        # Use a transaction for the specific database to ensure data consistency
        with transaction.atomic(using=using):
            # Check if the user already exists in the specified database
            if User.objects.using(using).filter(username=username).exists():
                print(f"User '{username}' already exists in {using}. Exiting...")
                return
            
            # Create and save the superuser in the specified database
            user = User(username=username)
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save(using=using)  # Save to the specific database

            # Double-check creation by reloading from the database
            user.refresh_from_db(using=using)
            print(f"Superuser '{username}' created successfully in {using}.")

    except Exception as e:
        print(f"Error creating superuser in {using}: {e}")

if __name__ == "__main__":
    create_superuser("admin", "a@123456", using='database2')