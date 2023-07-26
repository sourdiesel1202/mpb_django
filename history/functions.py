from mpb_django.functions import timestamp_to_datetime, execute_query
import os
import time

from mpb_django.enums import OrderType
import datetime,io
from zoneinfo import ZoneInfo
from mpb_django.functions import generate_csv_string, read_csv, write_csv, delete_csv, get_today, timestamp_to_datetime, human_readable_datetime, execute_query#, execute_update
import pandas as pd
from stockstats import wrap

class TickerHistory:
    open = 0
    close = 0
    high = 0
    low = 0
    volume = 0
    timestamp = 0
    dt = None
    def __init__(self, open, close, high, low, volume, timestamp):
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.timestamp =timestamp
        self.dt = timestamp_to_datetime(timestamp)
def load_ticker_history_cached(ticker, timespan, timespan_miltiplier, connection):
    records =execute_query(connection, f"select open, close, high, low, volume, timestamp from history_tickerhistory where timespan='{timespan}' and timespan_multiplier='{timespan_miltiplier}' and ticker_id=(select id from tickers_ticker where symbol='{ticker}') order by timestamp asc")
    return [TickerHistory(*[float(x) if '.' in x else int(x) for x in records[i]]) for i in range(1, len(records))]




def load_ticker_history_csv(ticker, ticker_history, convert_to_datetime=False, human_readable=False):

    # rows = load_ticker_history_raw(ticker,client,1, "hour", today,today,5000)
    rows = [['date', 'open', 'close', 'high', 'low', 'volume']]
    for entry in ticker_history:
        if convert_to_datetime:
            rows.append([timestamp_to_datetime(entry.timestamp) if not human_readable else human_readable_datetime(timestamp_to_datetime(entry.timestamp)) ,  entry.open, entry.close, entry.high, entry.low, entry.volume])
        else:
            rows.append([entry.timestamp, entry.open, entry.close, entry.high, entry.low, entry.volume])
    return  rows


def load_ticker_history_pd_frame(ticker, ticker_history, convert_to_datetime=False, human_readable=False):
    _str = generate_csv_string(load_ticker_history_csv(ticker,ticker_history,convert_to_datetime=convert_to_datetime, human_readable=human_readable))
    df = pd.read_csv(io.StringIO(_str), sep=",")
    return df
