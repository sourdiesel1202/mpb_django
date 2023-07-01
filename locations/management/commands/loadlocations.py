import json

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from locations.models import Location,LocationCity,LocationState,LocationCountry
class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(f"{settings.BASE_DIR}/json/locations.json") as f:
            # terpene_records = json.loads(f.read())

            for location_record in json.loads(f.read()):
                # print(json.dumps(location_record))
                if not LocationCountry.objects.filter(name=location_record['country']['name']).exists():
                    print(location_record['country']['emoji'])
                    country = LocationCountry()
                    country.name = location_record['country']['name']
                    country.code = location_record['country']['code']
                    country.emoji = location_record['country']['emoji']

                    country.save()
                else:
                    country = LocationCountry.objects.filter(name=location_record['country']['name'])[0]
                if not LocationState.objects.filter(name=location_record['state']['name']).exists():
                    state = LocationState()
                    state.name = location_record['state']['name']
                    state.code = location_record['state']['code']
                    # country.emoji = location_record['state']['emoji']
                    state.save()
                else:
                    state = LocationState.objects.filter(name=location_record['state']['name'])[0]

                if not LocationCity.objects.filter(name=location_record['city']['name']).exists():
                    city = LocationCity()
                    city.name = location_record['city']['name']
                    # city.code = location_record['city']['code']
                    # country.emoji = location_record['state']['emoji']
                    city.save()
                else:
                    city = LocationCity.objects.filter(name=location_record['city']['name'])[0]

                if not Location.objects.filter(country=country, state=state, city=city).exists():
                    location = Location()
                    location.country=country
                    location.state=state
                    location.city=city
                    location.save()
                    print(f"Wrote new location {location.city.name}, {location.state.name} {location.country.name} {location.country.emoji}")

