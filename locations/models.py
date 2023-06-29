from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now
# from locations.models import Location

# #basically a coupler between Report and and Alert
class LocationCountry(models.Model):
    name = models.CharField(max_length=150, null=False)
    emoji = models.CharField(max_length=2, null=False)
    code = models.CharField(max_length=5, null=False)

    def __str__(self):
        return f"{self.name}: {self.emoji}"

class LocationState(models.Model):
    name = models.CharField(max_length=150, null=False)
    # emoji = models.CharField(max_length=2, null=False)
    code = models.CharField(max_length=5, null=False)

    def __str__(self):
        return f"{self.name}: {self.code}"

class LocationCity(models.Model):
    name = models.CharField(max_length=150, null=False)
    longitude = models.CharField(max_length=150, null=False)
    latitude = models.CharField(max_length=150, null=False)
    code = models.CharField(max_length=5, null=False)
    def __str__(self):
        return f"{self.name}: {self.code}"

    # alert = models.ForeignKey(Alert, on_delete=models.CASCADE)

class Location(models.Model):
    # name = models.CharField(max_length=150, null=False)
    # emoji = models.CharField(max_length=2, null=False)
    county = models.ForeignKey(LocationCountry, on_delete=models.CASCADE)
    state = models.ForeignKey(LocationState, on_delete=models.CASCADE)
    city = models.ForeignKey(LocationCity, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.county}: {self.state}: {self.city}"
