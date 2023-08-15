class OrderType:
    CALL='CALL'
    PUT='PUT'
    BUY='BUY'
    SELL='SELL'
class AlertType:
    RSI_OVERBOUGHT = "RSI_OVERBOUGHT"
    RSI_OVERSOLD = "RSI_OVERSOLD"
    MACD_SIGNAL_CROSS_MACD ='MACD_SIGNAL_CROSS_MACD'
    MACD_MACD_CROSS_SIGNAL = 'MACD_MACD_CROSS_SIGNAL'
    SMA_CONFIRMATION_UPWARD = 'SMA_CONFIRMATION_UPWARD'
    SMA_CONFIRMATION_DOWNWARD = 'SMA_CONFIRMATION_DOWNWARD'
    DMIPLUS_CROSSOVER_DMINEG= 'DMIPLUS_CROSSOVER_DMINEG'
    DMINEG_CROSSOVER_DMIPLUS = 'DMINEG_CROSSOVER_DMIPLUS'
    ADX_THRESHOLD_UPWARD = 'ADX_THRESHOLD_UPWARD'
    GOLDEN_CROSS_APPEARED = 'GOLDEN_CROSS_APPEARED'
    DEATH_CROSS_APPEARED = 'DEATH_CROSS_APPEARED'
    SR_CONSOLIDATING = 'SR_CONSOLIDATING'
    BREAKOUT_SR_UP = 'BREAKOUT_SR_UP'
    BREAKOUT_SR_DOWN = 'BREAKOUT_SR_DOWN'
    ABOVE_HIGHEST_SR_BAND = 'ABOVE_HIGHEST_SR_BAND'
    BELOW_LOWEST_SR_BAND = 'BELOW_LOWEST_SR_BAND'
    # ABOVE_UPPER_SR_BAND = 'ABOVE_UPPER_SR_BAND'
    # BELOW_LOWER_SR_BAND = 'BELOW_LOWER_SR_BAND'
class PositionType:
    LONG = "LONG"
    SHORT = "SHORT"
    SHORT_OPTION = "PUT"
    LONG_OPTION = "CALL"

class PriceGoalChangeType:
    ASSET_SET_PRICE = 'ASSET_SET_PRICE'
    ASSET_POINTS = 'ASSET_POINTS'
    ASSET_PERCENTAGE = 'ASSET_PERCENTAGE'
    OPTION_TICK = 'OPTION_TICK'
    OPTION_PERCENTAGE = 'OPTION_PERCENTAGE'
    OPTION_SET_PRICE = 'OPTION_SET_PRICE'

class Timespan:
    HOUR = "hour"
    MINUTE = "minute"
    DAY = "day"

class TimespanMultiplier:
    ONE = "1"
    FIFTEEN = "15"
    THIRTY = "30"

time_frames = [
    {
        "timespan": Timespan.HOUR,
        "timespan_multiplier": TimespanMultiplier.ONE
    },
    {
        "timespan": Timespan.MINUTE,
        "timespan_multiplier": TimespanMultiplier.THIRTY
    }
]

class ValidationType:
    SMA = 'SMA'
    MACD = 'MACD'
    DMI = 'DMI'
    ADX = 'ADX'
    RSI = 'RSI'


class StrategyType:

    LONG_CALL = "LONG_CALL"
    LONG_PUT = "LONG_PUT"
    LONG_STRADDLE = "LONG_STRADDLE"
    LONG_STRANGLE = "LONG_STRANGLE"
    COLLAR = "COLLAR"
    SHORT_PUT = "SHORT_PUT"
    SHORT_CALL = "SHORT_CALL"
    SHORT_STRANGLE = "SHORT_STRANGLE"
    SHORT_STRADDLE = "SHORT_STRADDLE"
    LONG_CALL_SPREAD = "LONG_CALL_SPREAD"
    SHORT_CALL_SPREAD = "SHORT_CALL_SPREAD"
    LONG_PUT_SPREAD = "LONG_PUT_SPREAD"
    SHORT_PUT_SPREAD = "SHORT_PUT_SPREAD"
    IRON_BUTTERFLY = "IRON_BUTTERFLY"
    IRON_CONDOR = "IRON_CONDOR"

    #shorts
    # SHORT_STRADDLE = "SHORT_STRADDLE"
class TickerType:
    STOCK = "STOCK"
    OPTION = "OPTION"
    FUTURE = "FUTURE" #some day

ticker_types = [
    TickerType.STOCK,
    TickerType.OPTION,
    TickerType.FUTURE
]

strategy_types= [
    StrategyType.LONG_PUT,
    StrategyType.LONG_PUT,
    StrategyType.LONG_CALL_SPREAD,
    StrategyType.LONG_PUT_SPREAD,
    StrategyType.IRON_BUTTERFLY,
    StrategyType.IRON_CONDOR,
    StrategyType.LONG_STRANGLE,
    StrategyType.LONG_STRADDLE,
    StrategyType.COLLAR,
    StrategyType.SHORT_CALL,
    StrategyType.SHORT_PUT,
    StrategyType.SHORT_PUT_SPREAD,
    StrategyType.SHORT_CALL_SPREAD,
    StrategyType.SHORT_STRANGLE,
    StrategyType.SHORT_STRADDLE

]
validation_types = [
    ValidationType.ADX,
    ValidationType.DMI,
    ValidationType.RSI,
    ValidationType.SMA,
    ValidationType.MACD

]
position_types = [
    PositionType.LONG,
    PositionType.SHORT
]


alert_types=  [
    AlertType.RSI_OVERBOUGHT, AlertType.RSI_OVERSOLD, #rsi
    AlertType.SMA_CONFIRMATION_UPWARD, AlertType.SMA_CONFIRMATION_DOWNWARD, #sma
    AlertType.ADX_THRESHOLD_UPWARD, AlertType.DMINEG_CROSSOVER_DMIPLUS, AlertType.DMIPLUS_CROSSOVER_DMINEG, #adx, dmi
    AlertType.MACD_SIGNAL_CROSS_MACD, AlertType.MACD_MACD_CROSS_SIGNAL, #macd
    AlertType.BREAKOUT_SR_DOWN, AlertType.BREAKOUT_SR_UP, AlertType.SR_CONSOLIDATING, AlertType.BELOW_LOWEST_SR_BAND, AlertType.ABOVE_HIGHEST_SR_BAND, #sr bands
    AlertType.GOLDEN_CROSS_APPEARED, AlertType.DEATH_CROSS_APPEARED #crosses


]