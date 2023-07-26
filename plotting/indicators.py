import operator
import os
import traceback
from itertools import chain

from iteration_utilities import chained
from functools import partial

from mpb_django.enums import OrderType
import datetime
from zoneinfo import ZoneInfo
from history.functions import load_ticker_history_pd_frame, load_ticker_history_csv, load_ticker_history_cached
from stockstats import wrap
from mpb_django.enums import *
from plotting.shape import compare_tickers
from mpb_django.functions import human_readable_datetime, timestamp_to_datetime
from plotting.support_resistance import find_support_resistance_levels


# from validation import validate_dmi


# today =datetime.datetime.now().strftime("%Y-%m-%d")

def load_macd(ticker,ticker_history, module_config):
    df = wrap(load_ticker_history_pd_frame(ticker, ticker_history))
    return {'macd':df['macd'],'signal':df['macds'], 'histogram': df['macdh']}
def load_support_resistance(ticker, ticker_history, module_config, flatten=False):

    if flatten:
        flattened_levels = list(chain.from_iterable(find_support_resistance_levels(ticker, ticker_history, module_config)))
        flattened_levels.sort(key=lambda x: x)
        return flattened_levels
    else:
        return find_support_resistance_levels(ticker, ticker_history, module_config)

def load_sma(ticker,ticker_history, module_config, window=0):
    df = wrap(load_ticker_history_pd_frame(ticker, ticker_history))
    if window >0:
        # print(f"Returning {window} SMA")
        return df[f'close_{window}_sma']
    else:
        return df[f'close_{module_config["sma_window"]}_sma']
def load_golden_cross(ticker,ticker_history, module_config):
    return {"sma_long":load_sma(ticker,ticker_history,module_config, window=module_config['gc_long_sma_window']), f"sma_short":load_sma(ticker,ticker_history,module_config, window=module_config['gc_short_sma_window'])}
def load_death_cross(ticker,ticker_history, module_config):
    return {"sma_long":load_sma(ticker,ticker_history,module_config, window=module_config['dc_long_sma_window']), f"sma_short":load_sma(ticker,ticker_history,module_config, window=module_config['dc_short_sma_window'])}

# def load_sma(ticker, client,module_config, ticker_history, **kwargs):
#     sma = client.get_sma(ticker, **kwargs)
#     _sma = []
#     for entry in sma.values:
#         if module_config['logging']:
#             entry_date = datetime.datetime.fromtimestamp(entry.timestamp / 1e3, tz=ZoneInfo('US/Eastern'))
#             # entry_date.tzinfo = ZoneInfo('US/Eastern')
#             print(f"{entry_date}: {ticker}: SMA {entry.value}")
#         _sma.append(entry)
#
#
#
def load_rsi(ticker, ticker_history, module_config):
    df = wrap(load_ticker_history_pd_frame(ticker, ticker_history))
    return df['rsi']

    # return _sma
# def load_rsi(ticker, client,module_config, **kwargs):
#     rsi = client.get_rsi(ticker, timespan='hour')
#     _rsi = []
#     for entry in rsi.values:
#         if module_config['logging']:
#             entry_date = datetime.datetime.fromtimestamp(entry.timestamp / 1e3, tz=ZoneInfo('US/Eastern'))
#             # entry_date.tzinfo = ZoneInfo('US/Eastern')
#             print(f"{entry_date}: {ticker}: RSI {entry.value}")
#         _rsi.append(entry)
#     return _rsi
def load_obv(ticker, client,module_config, **kwargs):
    pass
# def load_adx(ticker, client, **kwargs):
    # load_dmi(ticker,client,**kwargs)


def is_trading_in_sr_band(indicator_data, ticker, ticker_history, module_config, **kwargs):
    #basically here we determine if the current price is in a support/resistance band
    if len(indicator_data) == 0:
        return False
    plus_minus = sum([round(float((x[1] - x[0])/2), 2) for x in indicator_data if len(x) > 1]) / len(indicator_data)
    for sr_band in indicator_data:
        if len(sr_band) == 2:
            if sr_band[0] <= ticker_history[-1].close <= sr_band[1]:
                if module_config['logging']:
                    print(f"{human_readable_datetime(timestamp_to_datetime(ticker_history[-1].timestamp))}:${ticker}: (Last Close ${ticker_history[-1].close}) is trading within Support/Resistance Band (Low: {sr_band[0]} | Mark: {ticker_history[-1].close} | High: {sr_band[1]})")
                return True

        elif len(sr_band) == 1:
            # plus_minus = (0.25/100)*sr_band[0]
            _tmp_band = [sr_band[0] - plus_minus, sr_band[0] + plus_minus]
            if  _tmp_band[0] <= ticker_history[-1].close <= _tmp_band[1]:
                if module_config['logging']:
                    print(f"{human_readable_datetime(timestamp_to_datetime(ticker_history[-1].timestamp))}:${ticker}: (Last Close ${ticker_history[-1].close}) is trading within Support/Resistance Band (Low: {_tmp_band[0]} | Mark: {ticker_history[-1].close} | High: {_tmp_band[1]})")
                return True
    return False

def load_dmi_adx(ticker, ticker_history, module_config, **kwargs):
    '''
    Returns a dict formatted like {'dmi+':<series_data>, 'dmi-':<series_data>, 'adx':<series_data>}
    where keys in the series are timestamps as loaded in load_ticker_history
    :param ticker:
    :param client:
    :param kwargs:
    :return:
    '''

    # print(f"{datetime.datetime.fromtimestamp(ticker_history[1].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}")
    # print(f"{datetime.datetime.fromtimestamp(ticker_history[1][-1] / 1e3, tz=ZoneInfo('US/Eastern'))} {ticker_history[1][0]}")
    df= wrap(load_ticker_history_pd_frame(ticker, ticker_history))
    dmi= {"dmi+":df['pdi'],"dmi-":df['ndi'], "adx":df['adx']}
    if module_config['logging']:
        print(f"{datetime.datetime.fromtimestamp(ticker_history[-1].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}:{ticker}: DMI+: {dmi['dmi+'][ticker_history[-1].timestamp]} DMI-:{dmi['dmi-'][ticker_history[-1].timestamp]} ADX: {dmi['adx'][ticker_history[-1].timestamp]}")
        print(f"{datetime.datetime.fromtimestamp(ticker_history[0].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}:{ticker}: DMI+: {dmi['dmi+'][ticker_history[0].timestamp]} DMI-:{dmi['dmi-'][ticker_history[0].timestamp]} ADX: {dmi['adx'][ticker_history[0].timestamp]}")
    # for i in reversed(range(0, len(ticker_history))):
    #     if module_config['logging']:
    #     # if True:


    return dmi

def did_macd_alert(indicator_data,ticker,ticker_history, module_config):
    if module_config['logging']:
        print(f"Checking MACD Alert, Comparing Value at {datetime.datetime.fromtimestamp(ticker_history[-1].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}:{ticker}: to value at {datetime.datetime.fromtimestamp(ticker_history[-2].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}")
    # print(f"{ticker_history[-1]}:{ticker}: RSI determined to be {AlertType.RSI_OVERSOLD}: RSI: {indicator_data[ticker_history[-1].timestamp]} ")
    # if (data[0].value > data[0].signal and data[1].value < data[1].signal)  or (data[0].value < data[0].signal and data[1].value > data[1].signal):
    if (indicator_data['macd'][ticker_history[-1].timestamp] > indicator_data['signal'][ticker_history[-1].timestamp] and indicator_data['macd'][ticker_history[-2].timestamp] < indicator_data['signal'][ticker_history[-2].timestamp] and (indicator_data['histogram'][ticker_history[-1].timestamp] > indicator_data['histogram'][ticker_history[-2].timestamp] and indicator_data['histogram'][ticker_history[-1].timestamp] > 0) ) or \
            (indicator_data['macd'][ticker_history[-1].timestamp] < indicator_data['signal'][ticker_history[-1].timestamp] and indicator_data['macd'][ticker_history[-2].timestamp] > indicator_data['signal'][ticker_history[-2].timestamp] and (indicator_data['histogram'][ticker_history[-1].timestamp] < indicator_data['histogram'][ticker_history[-2].timestamp] and indicator_data['histogram'][ticker_history[-1].timestamp] < 0)):
        return True
    else:
        return  False

# def did_macd_alert(data, ticker,module_config):
#     if module_config['logging']:
#         print(f"checking macd for {ticker}")
#     #ok so the idea here is to look at the data for n vs  n-1 where n is the most recent macd reading
#     if (data[0].value > data[0].signal and data[1].value < data[1].signal)  or (data[0].value < data[0].signal and data[1].value > data[1].signal):
#
#         if module_config['logging']:
#             entry_date = datetime.datetime.fromtimestamp(data[0].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))
#             print(f"{entry_date}:{ticker}: MAC/Signal Crossover ")
#         return True
#     else:
#         return False
#     pass

def did_sma_alert(indicator_data,ticker,ticker_history, module_config):
    if module_config['logging']:
        print(f"Checking SMA Alert, Comparing Value at {datetime.datetime.fromtimestamp(ticker_history[-1].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))} to value at {datetime.datetime.fromtimestamp(ticker_history[-2].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}")
    if (ticker_history[-1].close > indicator_data[ticker_history[-1].timestamp] and ticker_history[-1].low > indicator_data[ticker_history[-1].timestamp] and ticker_history[-1].close > ticker_history[-1].open and ticker_history[-2].low <= indicator_data[ticker_history[-2].timestamp])  or \
       (ticker_history[-1].close < indicator_data[ticker_history[-1].timestamp] and ticker_history[-1].high < indicator_data[ticker_history[-1].timestamp] and ticker_history[-1].close < ticker_history[-1].open and ticker_history[-2].high >= indicator_data[ticker_history[-2].timestamp]):
        return True
    else:
        return False

def determine_sma_alert_type(indicator_data,ticker,ticker_history, module_config):
    if (ticker_history[-1].close > indicator_data[ticker_history[-1].timestamp] and ticker_history[-1].open > indicator_data[ticker_history[-1].timestamp] and ticker_history[-1].close > ticker_history[-1].open and ticker_history[-2].low <= indicator_data[ticker_history[-2].timestamp]):
        return AlertType.SMA_CONFIRMATION_UPWARD
    elif (ticker_history[-1].close < indicator_data[ticker_history[-1].timestamp] and ticker_history[-1].close < indicator_data[ticker_history[-1].timestamp] and ticker_history[-1].close < ticker_history[-1].open and ticker_history[-2].high >= indicator_data[ticker_history[-2].timestamp]):
        return AlertType.SMA_CONFIRMATION_DOWNWARD
    else:
        raise Exception(f"Could not determine SMA Direction for {ticker}")


def did_golden_cross_alert(indicator_data,ticker,ticker_history, module_config):
    if module_config['logging']:
        print(f"Checking Golden Cross Alert, Comparing Value at {datetime.datetime.fromtimestamp(ticker_history[-1].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}:Long SMA {indicator_data['sma_long'][ticker_history[-1].timestamp]} Short SMA: {indicator_data['sma_short'][ticker_history[-1].timestamp]}: to value at {datetime.datetime.fromtimestamp(ticker_history[-2].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}:Long SMA {indicator_data['sma_long'][ticker_history[-2].timestamp]} Short SMA: {indicator_data['sma_short'][ticker_history[-2].timestamp]}:")
    return indicator_data['sma_short'][ticker_history[-1].timestamp] > indicator_data['sma_long'][ticker_history[-1].timestamp] and indicator_data['sma_short'][ticker_history[-2].timestamp] < indicator_data['sma_long'][ticker_history[-2].timestamp]

def did_death_cross_alert(indicator_data, ticker, ticker_history, module_config):
    if module_config['logging']:
        print(
            f"Checking Death Cross Alert, Comparing Value at {datetime.datetime.fromtimestamp(ticker_history[-1].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}:Long SMA {indicator_data['sma_long'][ticker_history[-1].timestamp]} Short SMA: {indicator_data['sma_short'][ticker_history[-1].timestamp]}: to value at {datetime.datetime.fromtimestamp(ticker_history[-2].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}:Long SMA {indicator_data['sma_long'][ticker_history[-2].timestamp]} Short SMA: {indicator_data['sma_short'][ticker_history[-2].timestamp]}:")
    return indicator_data['sma_short'][ticker_history[-1].timestamp] < indicator_data['sma_long'][ticker_history[-1].timestamp] and indicator_data['sma_short'][ticker_history[-2].timestamp] > indicator_data['sma_long'][ticker_history[-2].timestamp]

    # if ((ticker_history[-1].close > indicator_data[ticker_history[-1].timestamp] and ticker_history[-1].low > indicator_data[ticker_history[-1].timestamp] and ticker_history[-1].close > ticker_history[-1].open) and ticker_history[-2].open < indicator_data[ticker_history[-2].timestamp]) or\
    #         ((ticker_history[-1].close < indicator_data[ticker_history[-1].timestamp] and ticker_history[-1].high < indicator_data[ticker_history[-1].timestamp] and ticker_history[-1].close < ticker_history[-1].open) and ticker_history[-2].open > indicator_data[ticker_history[-2].timestamp]):
    #     return True
    # else:
    #     return False
# def did_sma_alert(sma_data,ticker_data, ticker,module_config):
#     # ok so in the case of
#     entry_date = datetime.datetime.fromtimestamp(sma_data[0].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))
#     entry_date_ticker = datetime.datetime.fromtimestamp(ticker_data[-1].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))
#     # print(f"{entry_date}:{ticker}: SMA Alert Check ")
#     # print(f"{entry_date_ticker}:{ticker}: SMA Alert Check ")
#     if ((ticker_data[-1].close > sma_data[0].value and ticker_data[-1].open > sma_data[0].value and ticker_data[-1].close > ticker_data[-1].open) and ticker_data[-2].open  < sma_data[1].value ) or \
#        ((ticker_data[-1].close < sma_data[0].value and ticker_data[-1].open < sma_data[0].value and ticker_data[-1].close < ticker_data[-1].open)  and ticker_data[-2].open  > sma_data[1].value ):
#         if module_config['logging']:
#             print(f"{entry_date_ticker}:{ticker}: SMA Crossover Alert Fired on {ticker}")
#         return True
#     else:
#         return False


def did_adx_alert(dmi_data,ticker,ticker_data,module_config):
    '''
    Pass in the data from the client and do calculations
    :param data:
    :return:
    '''

    valid_dmi = (dmi_data['dmi+'][ticker_data[-1].timestamp] > dmi_data['dmi-'][ticker_data[-1].timestamp] and dmi_data['dmi+'][ticker_data[-1].timestamp] > module_config['adx_threshold'] and dmi_data['adx'][ticker_data[-1].timestamp] > module_config['adx_threshold'] and dmi_data['adx'][ticker_data[-1].timestamp] > dmi_data['adx'][ticker_data[-2].timestamp]) or \
                (dmi_data['dmi+'][ticker_data[-1].timestamp] < dmi_data['dmi-'][ticker_data[-1].timestamp] and dmi_data['dmi-'][ticker_data[-1].timestamp] > module_config['adx_threshold'] and dmi_data['adx'][ticker_data[-1].timestamp] > module_config['adx_threshold'] and dmi_data['adx'][ticker_data[-1].timestamp] > dmi_data['adx'][ticker_data[-2].timestamp])
    if valid_dmi and dmi_data['adx'][ticker_data[-1].timestamp] > module_config['adx_threshold'] and dmi_data['adx'][ticker_data[-1].timestamp] > dmi_data['adx'][ticker_data[-2].timestamp]:
        if module_config['logging']:
            print(f"{datetime.datetime.fromtimestamp(ticker_data[-1].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}:{ticker}:: ADX Alert Triggered  ADX Value: {dmi_data['adx'][ticker_data[-1].timestamp]} adx-1 Value: {dmi_data['adx'][ticker_data[-2].timestamp]} ")
        return True

    else:
        return False


def did_dmi_alert(dmi_data,ticker,ticker_data,module_config):

    # ok so check for dmi+ crossing over dmi- AND dmi+ over adx OR dmi- crossing over dmi+ AND dmi- over adx
    if (dmi_data['dmi+'][ticker_data[-1].timestamp] > dmi_data['dmi-'][ticker_data[-1].timestamp] and dmi_data['dmi+'][ticker_data[-2].timestamp] < dmi_data['dmi-'][ticker_data[-2].timestamp] and dmi_data['dmi+'][ticker_data[-1].timestamp] >  dmi_data['adx'][ticker_data[-1].timestamp]) or (dmi_data['dmi+'][ticker_data[-1].timestamp] < dmi_data['dmi-'][ticker_data[-1].timestamp] and dmi_data['dmi+'][ticker_data[-2].timestamp] > dmi_data['dmi-'][ticker_data[-2].timestamp] and dmi_data['dmi-'][ticker_data[-1].timestamp] >  dmi_data['adx'][ticker_data[-1].timestamp]):
        if module_config['logging']:
            print(f"{datetime.datetime.fromtimestamp(ticker_data[-1].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}:{ticker}::{ticker}: DMI Alert Triggered (DMI+: {dmi_data['dmi+'][ticker_data[-1].timestamp]} DMI-:{dmi_data['dmi-'][ticker_data[-1].timestamp]} ADX: {dmi_data['adx'][ticker_data[-1].timestamp]})")
        return True
    else:
        return False



def did_rsi_alert(indicator_data,ticker,ticker_history, module_config):
    if module_config['logging']:
        print(f"${ticker}: Checking RSI Alert, Comparing Value at {datetime.datetime.fromtimestamp(ticker_history[-1].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}:{ticker}: to value at {datetime.datetime.fromtimestamp(ticker_history[-2].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}:{ticker}:")
    if indicator_data[ticker_history[-1].timestamp] > module_config['rsi_overbought_threshold'] or indicator_data[ticker_history[-1].timestamp] < module_config['rsi_oversold_threshold']:
        return True
    else:
        return False

# def did_rsi_alert(data, ticker,module_config):
#     if data[0].value > module_config['rsi_overbought_threshold'] or data[0].value < module_config['rsi_oversold_threshold']:
#         if module_config['logging']:
#             entry_date = datetime.datetime.fromtimestamp(data[0].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))
#             print(f"{entry_date}:{ticker}: RSI Alerted at {data[0].value} ")
#         return True
#     else:
#         return  False


def determine_macd_alert_type(indicator_data,ticker,ticker_history, module_config):
    if (indicator_data['macd'][ticker_history[-1].timestamp] > indicator_data['signal'][ticker_history[-1].timestamp] and indicator_data['macd'][ticker_history[-2].timestamp] < indicator_data['signal'][ticker_history[-2].timestamp] and (indicator_data['histogram'][ticker_history[-1].timestamp] > indicator_data['histogram'][ticker_history[-2].timestamp] and indicator_data['histogram'][ticker_history[-1].timestamp] > 0)) :
        return AlertType.MACD_MACD_CROSS_SIGNAL
    elif (indicator_data['macd'][ticker_history[-1].timestamp] < indicator_data['signal'][ ticker_history[-1].timestamp] and indicator_data['macd'][ticker_history[-2].timestamp] > indicator_data['signal'][ticker_history[-2].timestamp] and (indicator_data['histogram'][ticker_history[-1].timestamp] < indicator_data['histogram'][ticker_history[-2].timestamp] and indicator_data['histogram'][ticker_history[-1].timestamp] < 0)):
        return AlertType.MACD_SIGNAL_CROSS_MACD
    else:
        raise Exception("Unable to determine MACD alert type ")

# def determine_macd_alert_type(data, ticker,module_config):
#     # ok so the idea here is to look at the data for n vs  n-1 where n is the most recent macd reading
#     if (data[0].value > data[0].signal and data[1].value < data[1].signal) :
#
#         if module_config['logging']:
#             entry_date = datetime.datetime.fromtimestamp(data[0].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))
#             print(f"{entry_date}:{ticker}: MAC/Signal Crossover ")
#         return AlertType.MACD_MACD_CROSS_SIGNAL
#     elif (data[0].value < data[0].signal and data[1].value > data[1].signal):
#         return AlertType.MACD_SIGNAL_CROSS_MACD
#     else:
#         raise Exception(f"Could not determine MACD direction for: {ticker}")
def determine_rsi_alert_type(indicator_data,ticker,ticker_history, module_config):
    if indicator_data[ticker_history[-1].timestamp] >= module_config['rsi_overbought_threshold']:
        if module_config['logging']:
            entry_date = datetime.datetime.fromtimestamp(ticker_history[-1].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))
            print(f"{entry_date}:{ticker}: RSI determined to be {AlertType.RSI_OVERSOLD}: RSI: {indicator_data[ticker_history[-1].timestamp]} ")
        return AlertType.RSI_OVERBOUGHT
    elif indicator_data[ticker_history[-1].timestamp] < module_config['rsi_oversold_threshold']:
        if module_config['logging']:
            entry_date = datetime.datetime.fromtimestamp(ticker_history[-1].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))
            print(f"{entry_date}:{ticker}: RSI determined to be {AlertType.RSI_OVERSOLD}: RSI: {indicator_data[ticker_history[-1].timestamp]} ")
        return AlertType.RSI_OVERSOLD
    else:
        raise Exception(f"Could not determine RSI Direction for {ticker}")
# def determine_rsi_direction(data, ticker, module_config):
#     if data[0].value > module_config['rsi_overbought_threshold']:
#         if module_config['logging']:
#             entry_date = datetime.datetime.fromtimestamp(data[0].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))
#             print(f"{entry_date}:{ticker}: RSI determined to be {AlertType.RSI_OVERSOLD}: RSI: {data[0].value} ")
#         return AlertType.RSI_OVERBOUGHT
#     elif data[0].value < module_config['rsi_oversold_threshold']:
#         if module_config['logging']:
#             entry_date = datetime.datetime.fromtimestamp(data[0].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))
#             print(f"{entry_date}:{ticker}: RSI determined to be {AlertType.RSI_OVERSOLD}: RSI: {data[0].value} ")
#         return AlertType.RSI_OVERSOLD
#     else:
#         raise Exception(f"Could not determine RSI Direction for {ticker}")

def determine_adx_alert_type(data, ticker,ticker_data,  module_config):
    return AlertType.ADX_THRESHOLD_UPWARD
#
# def determine_dmi_alert_type(data, ticker, ticker_data, module_config):
def determine_dmi_alert_type(data, ticker, ticker_data, module_config):
    if (data['dmi+'][ticker_data[-1].timestamp] > data['dmi-'][ticker_data[-1].timestamp] and data['dmi+'][ticker_data[-2].timestamp] < data['dmi-'][ticker_data[-2].timestamp] and data['dmi+'][ticker_data[-1].timestamp] > data['adx'][ticker_data[-1].timestamp]):
        if module_config['logging']:
            print(f"{datetime.datetime.fromtimestamp(ticker_data[-1].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}:{ticker}: DMI Alert Determined Directio: {AlertType.DMIPLUS_CROSSOVER_DMINEG} (DMI+: {data['dmi+'][ticker_data[-1].timestamp]} DMI-:{data['dmi-'][ticker_data[-1].timestamp]} ADX: {data['adx'][ticker_data[-1].timestamp]})")
        return AlertType.DMIPLUS_CROSSOVER_DMINEG
    elif (data['dmi+'][ticker_data[-1].timestamp] < data['dmi-'][ticker_data[-1].timestamp] and data['dmi+'][ticker_data[-2].timestamp] > data['dmi-'][ticker_data[-2].timestamp] and data['dmi-'][ticker_data[-1].timestamp] > data['adx'][ticker_data[-1].timestamp]):
        if module_config['logging']:
            print(f"{datetime.datetime.fromtimestamp(ticker_data[-1].timestamp / 1e3, tz=ZoneInfo('US/Eastern'))}:{ticker}: DMI Alert Determined Directio: {AlertType.DMIPLUS_CROSSOVER_DMINEG} (DMI+: {data['dmi+'][ticker_data[-1].timestamp]} DMI-:{data['dmi-'][ticker_data[-1].timestamp]} ADX: {data['adx'][ticker_data[-1].timestamp]})")
        return AlertType.DMINEG_CROSSOVER_DMIPLUS


    else:
        raise Exception(f"Could not determine RSI Direction for {ticker}")


def determine_death_cross_alert_type(indicator_data,ticker,ticker_history, module_config):
    if indicator_data['sma_short'][ticker_history[-1].timestamp] < indicator_data['sma_long'][ticker_history[-1].timestamp] and indicator_data['sma_short'][ticker_history[-2].timestamp] > indicator_data['sma_long'][ticker_history[-2].timestamp]:
        return AlertType.DEATH_CROSS_APPEARED
    else:
        raise Exception(f"Could not determine Golden Cross Alert for {ticker}")
def determine_sr_direction(indicator_data,ticker,ticker_history, module_config):
    if len(indicator_data) == 0:
        raise Exception("Cannot determine Support/Resistance Direction with no data!")
    plus_minus = sum([round(float((x[1] - x[0]) / 2), 2) for x in indicator_data if len(x) > 1]) / len(indicator_data)
    # ok so if we're trading in an SR band, we wan
    trending_positive = (ticker_history[-1].close >ticker_history[-1].open) and  (ticker_history[-2].open < ticker_history[-2].close) and ticker_history[-2].close < ticker_history[-1].close# sum([ticker_history[-ii].close - ticker_history[-(ii + 1)].close for ii in range(1, 2)]) >= 0
    for sr_band in indicator_data:
        if len(sr_band) == 2:
            if sr_band[0] <= ticker_history[-1].close <= sr_band[1]:

                # if module_config['logging']:
                    # print(
                        # f"{human_readable_datetime(timestamp_to_datetime(ticker_history[-1].timestamp))}:${ticker}: (Last Close ${ticker_history[-1].close}) is trading within Support/Resistance Band (Low: {sr_band[0]} | Mark: {ticker_history[-1].close} | High: {sr_band[1]})")

                #if we're in a band, find out whether it's heading toward the top or the bottom of the band
                #look back over last 3 bars, and see what the trend is, if it's down we're presumably headed to the support level,
                #if it's up presumably we're headed
                return AlertType.SR_CONSOLIDATING+f" (LB: ${round(sr_band[0],2)} | Current: ${ticker_history[-1].close} | HB: ${round(sr_band[1],2)})"

        elif len(sr_band) == 1:
            # plus_minus = (0.25/100)*sr_band[0]
            _tmp_band = [sr_band[0] - plus_minus, sr_band[0] + plus_minus]
            if _tmp_band[0] <= ticker_history[-1].close <= _tmp_band[1]:
                return AlertType.SR_CONSOLIDATING+f" (LB: ${round(_tmp_band[0],2)} | Current: ${ticker_history[-1].close} | HB: ${round(_tmp_band[1],2)})"
                pass

    #if we get here we are in a breakout, so we need to find out what band it's approaching
    #first get direction
    # deltas =
    #positive upward movement
    # ok so now we need to figure out what the nearest SR band is
    # _tmp_band = [sr_band[0] - plus_minus, sr_band[0] + plus_minus]
    distance_to_points = []

    flattened_levels = list(chain.from_iterable(indicator_data))
    flattened_levels.sort(key=lambda x: x)

    for level in flattened_levels:
        if trending_positive:
            if level < ticker_history[-1].close:
                continue
            else:
                distance_to_points.append(level - ticker_history[-1].close)
        else:
            if level > ticker_history[-1].close:
                continue
            else:
                distance_to_points.append(level - ticker_history[-1].close)


    if len(distance_to_points) == 0:
        if trending_positive:

            return AlertType.ABOVE_HIGHEST_SR_BAND+f": ${flattened_levels[-1]}"
        else:
            return AlertType.BELOW_LOWEST_SR_BAND+f" ${flattened_levels[0]}"
    else:
        # sr_band = indicator_data[min_index] if len(indicator_data[min_index]) > 1 else [sr_band[0] - plus_minus, sr_band[0] + plus_minus]
        distance_to_points.sort(key=lambda x: x, reverse=not trending_positive)
        if trending_positive:
            return AlertType.BREAKOUT_SR_UP+f"==>${round(distance_to_points[0]+ticker_history[-1].close,2)} (${round(distance_to_points[0],2)}/{round(float(distance_to_points[0] / ticker_history[-1].close)*100,2)}%)"
        else:
            return AlertType.BREAKOUT_SR_DOWN+f"==>${round(distance_to_points[0]+ticker_history[-1].close,2)} (${round(distance_to_points[0],2)}/{round(float(distance_to_points[0] / ticker_history[-1].close)*100,2)}%)"
def determine_golden_cross_alert_type(indicator_data,ticker,ticker_history, module_config):
    if did_golden_cross_alert(indicator_data,ticker,ticker_history,module_config):
        return AlertType.GOLDEN_CROSS_APPEARED
    else:
        raise Exception(f"Could not determine Golden Cross Alert for {ticker}")
# def determine_death_cross_alert_type(indicator_data,ticker,ticker_history, module_config):

def has_matching_trend_with_ticker(ticker_a, ticker_history_a,ticker_b, ticker_history_b, module_config):
    return compare_tickers(ticker_a, ticker_history_a,ticker_b, ticker_history_b, module_config) >= module_config['line_similarity_gt']

def load_ticker_similar_trends(ticker, module_config):
    ticker_history = load_ticker_history_cached(ticker, module_config)
    result = []
    # if module_config['logging']:
    print(f"{human_readable_datetime(datetime.datetime.now())}:${ticker}: Performing line comparison of ${ticker}")
    for compare_ticker in [x.split(f"{module_config['timespan_multiplier']}{module_config['timespan']}.csv")[0] for x in os.listdir(f"{module_config['output_dir']}cached/") if "O:" not in x]:
        try:
            if module_config['logging']:
                print(f"{human_readable_datetime(datetime.datetime.now())}:${ticker}: Performing line comparison of ${ticker} <==> ${compare_ticker}")
            similarity = compare_tickers(ticker, ticker_history, compare_ticker, load_ticker_history_cached(compare_ticker, module_config), module_config)
            if similarity >= module_config['line_similarity_gt']:
                result.append([compare_ticker, similarity])
        except:
            pass
            # traceback.print_exc()


    #ok so once we get here, we need to sort by similarity, take top 3?
    # itemgetter_int = chained(operator.itemgetter(1),
    #                          partial(map, float), tuple)
    result.sort(key=operator.itemgetter(1))
    result.reverse()
    return [x[0] for x in result[:module_config['similar_line_tickers_limit']]]