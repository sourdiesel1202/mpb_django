import random

from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now

from mpb_django.functions import timestamp_to_datetime
from mpb_django.enums import position_types
from history.models import  TickerHistory
from tickers.models import Contract, Ticker


# from locations.models import Location
# from achievements.models import Achievement
# from taggit.managers import TaggableManager


    # username = models.CharField(max_length=150, null=False)

class SimilarLine(models.Model):
    ticker_history = models.ForeignKey(TickerHistory,null=False, on_delete=models.CASCADE)
    ticker = models.ForeignKey(Ticker,null=False, on_delete=models.CASCADE)
    forward_range = models.IntegerField(default=4, null=False)
    backward_range = models.IntegerField(default=10, null=False)
    def __str__(self):
        return f"{self.ticker_history.ticker.symbol}:{self.ticker_history.timestamp}: Similar Line: {self.ticker.symbol}"

class ProfitableLineType(models.Model):
    # line_type = models.IntegerField(default=1, null=False)
    name = models.CharField(null=False, max_length=250, default=f"Profitable Line", unique=True)


class ProfitableLine(models.Model):
    histories = models.ManyToManyField("history.TickerHistory", symmetrical=False)
    forward_range = models.IntegerField(default=4, null=False)
    backward_range = models.IntegerField(default=10, null=False)
    profit_percentage = models.FloatField(default=0.0, null=False)
    line_type = models.ForeignKey(ProfitableLineType, on_delete=models.CASCADE)
    # def __str__(self):
        # return f"{self.ticker_history.ticker.symbol}:{self.ticker_history.timestamp}: Similar Line: {self.ticker.symbol}"


# class TickerPositionContract(models.Model):
#     position = models.ForeignKey(TickerHistory,null=False, on_delete=models.CASCADE)
#     contract = models.ForeignKey(Contract,null=False, on_delete=models.CASCADE)

#ok so the idea here is that the positions are tied to ticker histories (timestamp as key),
#when we pull positions back by ticker history, we can then pull back the individual contracts for each position

    # def __str__(self):
    #     return f"{self.ticker_history}: {self.alert_type}"

