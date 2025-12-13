import json
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from apply.models import Region, District

class Command(BaseCommand):
    help = 'Loads regions and districts from a JSON file into the database, clearing old data first.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        json_file_path = settings.BASE_DIR / 'regions.json'

        self.stdout.write(self.style.NOTICE(f"Loading data from {json_file_path}"))

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {json_file_path}. Please create it."))
            return
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR(f"Error decoding JSON from {json_file_path}."))
            return

        self.stdout.write("Clearing existing Region and District data...")
        District.objects.all().delete()
        Region.objects.all().delete()

        for region_data in data:
            region_name = region_data['name']
            region, created = Region.objects.get_or_create(name=region_name)
            
            if created:
                self.stdout.write(f'  Creating Region: {region.name}')

            for district_name in region_data['districts']:
                District.objects.get_or_create(region=region, name=district_name)
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded all regions and districts.'))