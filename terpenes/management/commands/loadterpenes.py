import json

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from terpenes.models import Terpene, Effect,Aroma
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(f"{settings.BASE_DIR}/json/terpene.json") as f:
            # terpene_records = json.loads(f.read())
            for terpene_record in  json.loads(f.read()):
                if not Terpene.objects.filter(name=terpene_record['name']).exists():
                    terpene = Terpene()
                    terpene.name=terpene_record['name']
                    terpene.description=terpene_record['description']
                    terpene.image=terpene_record['image']
                    terpene.save()
                    print(f"Processing: {terpene_record['name']}")
                    #process aromas
                    for aroma_record in terpene_record['aromas']:

                        if not Aroma.objects.filter(name=aroma_record['name']).exists():
                            aroma = Aroma()
                            aroma.name = aroma_record['name']
                            aroma.image = aroma_record['image']
                            aroma.description = aroma_record['description']
                            aroma.save()
                            terpene.aromas.add(aroma)
                        else:
                            terpene.aromas.add(Aroma.objects.filter(name=aroma_record['name'])[0])


                    for effect_record in terpene_record['aromas']:

                        if not Effect.objects.filter(name=effect_record['name']).exists():
                            effect = Effect()
                            effect.name = effect_record['name']
                            effect.image = effect_record['image']
                            effect.description = effect_record['description']
                            effect.save()
                            terpene.effects.add(effect)
                        else:
                            terpene.effects.add(Effect.objects.filter(name=effect_record['name'])[0])
                    terpene.save()
        # if not User.objects.filter(username="admin").exists():
        #     User.objects.create_superuser("admin", "admin@admin.com", "admin")