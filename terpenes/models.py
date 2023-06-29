from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now
# from locations.models import Location
from users.models import User
class Aroma(models.Model):
    name = models.CharField(max_length=150, null=False)
    description = models.TextField(max_length=500, null=False)
    image = models.TextField(max_length=500, null=False)

class Effect(models.Model):
    name = models.CharField(max_length=150, null=False)
    description = models.TextField(max_length=500, null=False)
    image = models.TextField(max_length=500, null=False)


class Terpene(models.Model):
    name = models.CharField(max_length=150, null=False)
    description = models.TextField(max_length=1500, null=False)
    image = models.TextField(max_length=500, null=False)
    aromas = models.ManyToManyField("terpenes.Aroma", null=True, blank=True)
    effects = models.ManyToManyField("terpenes.Effect", null=True, blank=True)
    def __str__(self):
        return f"{self.name}"


class TerpeneProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    aromas = models.ManyToManyField("terpenes.Aroma", null=True, blank=True)
    effects = models.ManyToManyField("terpenes.Effect", null=True, blank=True)
    terpenes = models.ManyToManyField("terpenes.Terpene", null=True, blank=True)
