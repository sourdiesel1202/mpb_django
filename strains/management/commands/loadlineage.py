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
                if Strain.objects.filter(name=strain_record['name']).exists():

                    strain = Strain.objects.filter(name=strain_record['name'])[0]
                    print(f"Processing lineage for {strain.name}")
                    # ok so now we need to process parents and children
                    try:
                        for parent in strain_record['parents']:
                            _parent = Strain.objects.filter(name=parent)[0]
                            if _parent not in strain.parents.all():
                                strain.parents.add(_parent)
                        for child in strain_record['children']:
                            _child =Strain.objects.filter(name=child)[0]
                            if _child not in strain.children.all():
                                strain.children.add(_child)
                    except:
                        print(f"Cannot process lineage for {strain.name}")
                    strain.save()
        print(f"\nCompleted strain lineage load in {int((int(time.time()) - start_time) / 60)} minutes and {int((int(time.time()) - start_time) % 60)} seconds")



