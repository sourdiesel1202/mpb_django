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
    terpenes = models.ManyToManyField("terpenes.Terpene", null=True, blank=True)
    effects = models.ManyToManyField("terpenes.Effect", null=True, blank=True)
    parents = models.ManyToManyField("self", null=True, blank=True)
    children = models.ManyToManyField("self", null=True, blank=True)
    aromas = models.ManyToManyField("terpenes.Aroma", null=True, blank=True)
    type = models.CharField(choices=(('Indica', 'Indica'), ('Sativa', 'Sativa'), ('Hybrid', 'Hybrid')),default='Hybrid', max_length=150)
    aliases = models.CharField(max_length=150, null=False, default="")
    def __str__(self):
        return f"{self.name}: {self.type}"