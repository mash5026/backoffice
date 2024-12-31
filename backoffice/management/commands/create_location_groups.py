# management/commands/create_location_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from backoffice.models import Location  # Update 'your_app' to the name of your Django app

class Command(BaseCommand):
    help = 'Create groups for each location based on the Location model where parentid is not null'

    def handle(self, *args, **kwargs):
        # Fetch all unique locations from the Location model where parentid is not null
        locations = Location.objects.filter(parentid__isnull=True).values_list('name', flat=True).distinct()  # Get distinct names with parentid not null

        for location in locations:
            group_name = f'CanCreateUser-{location}'
            group, created = Group.objects.get_or_create(name=group_name)

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {group.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Group already exists: {group.name}'))