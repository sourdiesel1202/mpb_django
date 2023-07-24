from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now

from mpb_django.functions import timestamp_to_datetime
from mpb_django.enums import Timespan, TimespanMultiplier, AlertType, alert_types
from history.models import  TickerHistory

# from locations.models import Location
# from achievements.models import Achievement
# from taggit.managers import TaggableManager


    # username = models.CharField(max_length=150, null=False)

class TickerAlert(models.Model):
    ticker_history = models.ForeignKey(TickerHistory,null=False, on_delete=models.CASCADE)
    alert_type = models.CharField(choices=((x,x) for x in alert_types),null=False, max_length=500)


    def __str__(self):
        return f"{self.ticker_history}: {self.alert_type}"

