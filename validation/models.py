from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now

from mpb_django.functions import timestamp_to_datetime
from mpb_django.enums import ValidationType, validation_types, position_types, strategy_types
from history.models import  TickerHistory




    # username = models.CharField(max_length=150, null=False)

class TickerValidation(models.Model):
    ticker_history = models.ForeignKey(TickerHistory,null=False, on_delete=models.CASCADE)
    validation_type = models.CharField(choices=((x,x) for x in validation_types),null=False, max_length=50)
    strategy_type = models.CharField(choices=((x,x) for x in strategy_types),null=False, max_length=150, default=strategy_types[0])

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['ticker_history', 'validation_type', 'strategy_type'], name="th_validation_type_strat_type_unique")
    #     ]
    def __str__(self):
        return f"{self.ticker_history}: {self.validation_type}"

