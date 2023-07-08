from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User
from strains.models import Strain
# from locations.models import Location

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    strain = models.ForeignKey(Strain, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(max_length=500, null=False)
    image = models.TextField(max_length=500, null=False, default="")
    likes = models.ManyToManyField("likes.Like", symmetrical=False)
    comments = models.ManyToManyField("comments.Comment", symmetrical=False)
    is_public = models.BooleanField(default=False, max_length=500, null=False)
    is_circle = models.BooleanField(default=False, max_length=500, null=False)
    creation_date = models.DateTimeField(null=True, default=now)