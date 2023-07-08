from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now
# from locations.models import Location
from users.models import User
class Comment(models.Model):
    # name = models.CharField(max_length=150, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, null=False)
    image = models.TextField(max_length=500, null=False)
    replies = models.ManyToManyField("self", symmetrical=False)
    creation_date = models.DateTimeField(null=True, default=now)
