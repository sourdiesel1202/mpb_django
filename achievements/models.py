from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now
# from locations.models import Location

# #basically a coupler between Report and and Alert
class Achievement(models.Model):
    name = models.CharField(max_length=150, null=False)
    emoji = models.CharField(max_length=2, null=False)
    code = models.CharField(max_length=5, null=False)

    def __str__(self):
        return f"{self.name}: {self.emoji}"