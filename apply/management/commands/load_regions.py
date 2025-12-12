import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from apply.models import Region, District

# Define the absolute path to the data file.
# settings.BASE_DIR points to the project root (where manage.py is).
DATA_FILE = os.path.join(settings.BASE_DIR, 'data', 'data.csv')

class Command(BaseCommand):
    help = 'Loads Region and District data from the external data/data.csv file.'

    def handle(self, *args, **options):
        
        if not os.path.exists(DATA_FILE):
            raise CommandError(f'File not found at: {DATA_FILE}. Check your path relative to manage.py.')
            
        regions_processed = 0
        districts_processed = 0
        
        self.stdout.write(self.style.SUCCESS(f"Starting data loading from: {DATA_FILE}"))
        
        # Use a cache to avoid repetitive database lookups for Regions
        region_cache = {} 

        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                
                for row in reader:
                    if len(row) < 2:
                        self.stdout.write(self.style.WARNING(f"Skipping malformed row: {row}"))
                        continue

                    region_name = row[0].strip()
                    district_name = row[1].strip()

                    # 1. Get/Create Region
                    if region_name not in region_cache:
                        region, created = Region.objects.get_or_create(name=region_name)
                        region_cache[region_name] = region
                        if created:
                            regions_processed += 1
                            self.stdout.write(f"  -> Created Region: {region_name}")
                    else:
                        region = region_cache[region_name]

                    # 2. Get/Create District
                    district, created = District.objects.get_or_create(
                        region=region,
                        name=district_name
                    )

                    if created:
                        districts_processed += 1
                        
                self.stdout.write(self.style.SUCCESS("-" * 40))
                self.stdout.write(self.style.SUCCESS(f"✅ Data Insertion Complete."))
                self.stdout.write(f"New Regions created: {regions_processed}")
                self.stdout.write(f"New Districts created: {districts_processed}")
                self.stdout.write(self.style.SUCCESS(f"Final Total Regions in DB: {Region.objects.count()}"))
                self.stdout.write(self.style.SUCCESS(f"Final Total Districts in DB: {District.objects.count()}"))
                self.stdout.write(self.style.SUCCESS("-" * 40))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
            raise CommandError('Data loading failed due to an unexpected error.')