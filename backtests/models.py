from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now

from mpb_django.functions import timestamp_to_datetime
from mpb_django.enums import position_types
from history.models import  TickerHistory
from positions.models import TickerPosition
from tickers.models import Contract, Ticker
from validation.models import TickerValidation


# from locations.models import Location
# from achievements.models import Achievement
# from taggit.managers import TaggableManager


    # username = models.CharField(max_length=150, null=False)

class Backtest(models.Model):
    validation = models.ForeignKey(TickerValidation,null=False, on_delete=models.CASCADE)
    results = models.TextField(default="{}", null=False) #json field
    # position_type = models.CharField(choices=((x,x) for x in position_types),null=False, max_length=500)

    def __str__(self):
        return f"{self.position.ticker_history.ticker.symbol}:{self.position.ticker_history.timestamp}: {self.position.type} Backtest"


# class TickerPositionContract(models.Model):
#     position = models.ForeignKey(TickerHistory,null=False, on_delete=models.CASCADE)
#     contract = models.ForeignKey(Contract,null=False, on_delete=models.CASCADE)

#ok so the idea here is that the positions are tied to ticker histories (timestamp as key),
#when we pull positions back by ticker history, we can then pull back the individual contracts for each position

    # def __str__(self):
    #     return f"{self.ticker_history}: {self.alert_type}"

