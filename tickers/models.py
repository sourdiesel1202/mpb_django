from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now


    # username = models.CharField(max_length=150, null=False)

class Ticker(models.Model):
    # ticker_history = models.ForeignKey(TickerHistory,null=False, on_delete=models.CASCADE)
    symbol = models.CharField(null=False, max_length=500)
    name = models.CharField(default='',null=False, max_length=500)
    sector = models.CharField(default='',null=False, max_length=500)
    description = models.TextField(default='',null=False, max_length=5000)


    def __str__(self):
        return f"{self.symbol}: {self.name} {self.sector}"

