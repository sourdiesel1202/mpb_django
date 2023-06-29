from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User
from strains.models import Strain
# from locations.models import Location

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500, null=False)
    image = models.TextField(max_length=500, null=False, default="")
    read = models.BooleanField(default=False, max_length=500, null=False)
    creation_date = models.DateTimeField(null=True, default=now)
class MessageThread(models.Model):
    # sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    messages = models.ManyToManyField("terp_messages.Message", null=True, blank=True)
    creation_date = models.DateTimeField(null=True, default=now)
