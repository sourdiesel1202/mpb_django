from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now
# from locations.models import Location

# #basically a coupler between Report and and Alert
class Strain(models.Model):
    name = models.CharField(max_length=150, null=False)

    url = models.TextField(max_length=500, null=False)
    description = models.TextField(max_length=500, null=False)
    image = models.TextField(max_length=500, null=False)
    # image = models.TextField(max_length=500, null=False)
    terpenes = models.ManyToManyField("terpenes.Terpene", symmetrical=False)
    effects = models.ManyToManyField("terpenes.Effect", symmetrical=False)
    parents = models.ManyToManyField("self",  blank=True,symmetrical=False, related_name="s_parents")
    children = models.ManyToManyField("self",related_name="s_children", blank=True, symmetrical=False)
    aromas = models.ManyToManyField("terpenes.Aroma", symmetrical=False)
    type = models.CharField(choices=(('Indica', 'Indica'), ('Sativa', 'Sativa'), ('Hybrid', 'Hybrid')),default='Hybrid', max_length=150)
    aliases = models.CharField(max_length=150, null=False, default="")
    def __str__(self):
        return f"{self.name}: {self.type}"

