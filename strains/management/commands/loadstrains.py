import json
import time

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from strains.models import Strain
from terpenes.models import Terpene
from django.conf import settings
class Command(BaseCommand):
    def handle(self, *args, **options):
        start_time = time.time()
        with open(f"{settings.BASE_DIR}/json/strain_data.json") as f:
            # terpene_records = json.loads(f.read())
            for strain_record in json.loads(f.read()):
                if not Strain.objects.filter(name=strain_record['name']).exists():
                    strain = Strain()
                    print(f"Processing strain: {strain_record['name']}")
                    # print(strain_record)
                    strain.url = strain_record['url']
                    strain.name = strain_record['name']
                    strain.description = strain_record['description']
                    strain.aliases = strain_record['aliases']
                    strain.type = strain_record['type']
                    strain.save()
                    #ok so now we need to handle the terpenes
                    for terpene in strain_record['terpenes']:
                        _terpene = Terpene.objects.filter(name=terpene)[0]
                        strain.terpenes.add(_terpene)
                    strain.save()
        print(f"\nCompleted strain load in {int((int(time.time()) - start_time) / 60)} minutes and {int((int(time.time()) - start_time) % 60)} seconds")
