from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now

from mpb_django.enums import ticker_types


# username = models.CharField(max_length=150, null=False)

class Ticker(models.Model):
    # ticker_history = models.ForeignKey(TickerHistory,null=False, on_delete=models.CASCADE)
    symbol = models.CharField(null=False, max_length=500)
    name = models.CharField(default='',null=False, max_length=500)
    description = models.TextField(default='',null=False, max_length=5000)
    sector = models.CharField(default='',null=False, max_length=500)
    type = models.CharField(choices=((x, x) for x in ticker_types), null=False, max_length=500, default=ticker_types[0])

    def __str__(self):
        return f"{self.symbol} ({self.type}): {self.name} {self.sector}"

class Contract(models.Model):
    # ticker_history = models.ForeignKey(TickerHistory,null=False, on_delete=models.CASCADE)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, null=False) #this should point back to the contract itself in tickers_ticker
    symbol = models.CharField(default='',null=False, max_length=500)
    name = models.CharField(default='',null=False, max_length=500)
    type = models.CharField(default='',null=False, max_length=500)
    expry = models.CharField(default='',null=False, max_length=500)
    description = models.TextField(default='',null=False, max_length=5000)
    strike_price = models.FloatField(default=0,null=False)

    def __str__(self):
        return f"{self.ticker.symbol}: {self.symbol}: {self.name}"
