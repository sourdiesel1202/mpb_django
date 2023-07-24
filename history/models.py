from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now

from mpb_django.functions import timestamp_to_datetime
from mpb_django.enums import Timespan, TimespanMultiplier
from tickers.models import Ticker


# from locations.models import Location
# from achievements.models import Achievement
# from taggit.managers import TaggableManager



    # username = models.CharField(max_length=150, null=False)

class TickerHistory(models.Model):
    ticker = models.ForeignKey(Ticker, null=False, on_delete=models.CASCADE)
    open = models.FloatField(default=0.0, null=False)
    close = models.FloatField(default=0.0, null=False)
    high = models.FloatField(default=0.0, null=False)
    low = models.FloatField(default=0.0, null=False)
    volume = models.FloatField(default=0.0, null=False)
    #need to test this locally
    timestamp = models.BigIntegerField(default=float(datetime.now().strftime('%s.%f')) * 1e3,null=False)
    timespan = models.CharField(choices=((Timespan.HOUR, Timespan.HOUR), (Timespan.DAY,Timespan.DAY), (Timespan.MINUTE,Timespan.MINUTE)),default=Timespan.HOUR, max_length=150)
    timespan_multiplier = models.CharField(choices=((TimespanMultiplier.ONE,TimespanMultiplier.ONE), (TimespanMultiplier.FIFTEEN,TimespanMultiplier.FIFTEEN), (TimespanMultiplier.THIRTY, TimespanMultiplier.THIRTY)),default=TimespanMultiplier.ONE, max_length=150)

    def __str__(self):
        return f"{self.ticker}: {timestamp_to_datetime(self.timestamp)} {self.close}"

