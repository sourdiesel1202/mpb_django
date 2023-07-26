from plotly.subplots import make_subplots
import plotly.graph_objects as go
# import pandas as pd

# import s3
from history.functions import load_ticker_history_pd_frame, load_ticker_history_cached
from plotting.indicators import load_macd, load_sma, load_dmi_adx, load_rsi,load_support_resistance
from plotting.indicators import load_dmi_adx
from plotting.indicators import  load_death_cross, load_golden_cross, determine_death_cross_alert_type,determine_golden_cross_alert_type, did_golden_cross_alert, did_death_cross_alert
from mpb_django.functions import load_module_config
def build_ticker_charts(connection, ticker,timespan, timespan_multiplier):
    module_config = load_module_config(f"{timespan_multiplier}{timespan}mpb")
    #ok so first we need to load the ticker history
    ticker_history = load_ticker_history_cached(ticker, timespan, timespan_multiplier,connection)
    return plot_ticker_with_indicators(ticker, ticker_history,build_indicator_dict(ticker, ticker_history, module_config), module_config) #basically just return our generated html
def plot_ticker_with_indicators(ticker, ticker_history, indicator_data, module_config):

    df = load_ticker_history_pd_frame(ticker, ticker_history[-module_config['plot_bars']:], convert_to_datetime=True, human_readable=True)
    subplot_titles = [x  for x in indicator_data.keys() if not indicator_data[x]['overlay']]
    # candle_fig  = make_subplots(rows=len([not x['overlay'] for x in indicator_data.values()]), cols=2, subplot_titles=subplot_titles)
    candle_fig = go.Figure(data=[go.Candlestick(x=df['date'],
                                         open=df['open'], high=df['high'],
                                         low=df['low'], close=df['close'],name=ticker)] )
    r = 1
    # c =2
    indicator_figure = make_subplots(rows=len([not x['overlay'] for x in indicator_data.values()]), cols=1, subplot_titles=subplot_titles)
    for key,x in indicator_data.items():
        if x['overlay']:
            if type(x['plot']) not in [list, tuple]:
                candle_fig.add_trace(x['plot'])
            else:
                for i in range(0, len(x['plot'])):
                    if type(x['plot'][i]) == go.Scatter:

                        candle_fig.add_trace(x['plot'][i])
                    else:
                        candle_fig.add_shape(x['plot'][i])
        else:
            if type(x['plot']) not in [list,tuple]:
                indicator_figure.add_trace(x['plot'], row=r, col=1)
            else:
                for i in range(0, len(x['plot'])):
                    indicator_figure.add_trace(x['plot'][i], row=r, col=1)
            r = r + 1
    candle_fig.update_layout(xaxis_rangeslider_visible=False, xaxis=dict(type="date"))
    min_percent=(50/100)*min([x.low for x in ticker_history])
    max_percent=(50/100)*max([x.low for x in ticker_history])
    # fig.update_yaxes( type='log')

    candle_fig.update_xaxes(rangebreaks=[
            dict(bounds=["sat", "mon"]),
            dict(bounds=[16, 9.5], pattern="hour"),

        ])
    # candle_fig.show()
    # indicator_figure.show()
    return figures_to_html(ticker, [candle_fig, indicator_figure])


def plot_indicator_data(ticker, ticker_history,indicator_data, module_config, name='', color='blue', max=100):
    df = load_ticker_history_pd_frame(ticker, ticker_history, convert_to_datetime=True, human_readable=True)
    return go.Figure(data=go.Scatter(
        x=df['date'],
        y=[indicator_data[x.timestamp] for x in ticker_history],
        name=name, mode='lines', line={'color':color, 'width':1},
    ), layout_yaxis_range=[0, max]).data[0]


def plot_indicator_data_dual_y_axis(ticker, ticker_history,indicator_data, module_config,keys=[],colors=['blue']):

    fig  = make_subplots(rows=1, cols=1)
    # fig.add_trace()
    counter = 2

    for i in range(0, len(keys)):

        fig.add_trace(plot_indicator_data(ticker, ticker_history,indicator_data[keys[i]],module_config, color=colors[i], name=keys[i]), row=1, col=1)


    return fig.data

def plot_sr_lines(ticker, ticker_history,indicator_data, module_config):
    lines = []
    for sr_level in indicator_data:
        text = ['' for x in ticker_history[:1]]
        # text.insert(-1, sr_level)
        lines.append(go.Scatter(
                    x=[x.dt for x in ticker_history],
                    y=[sr_level for x in ticker_history],
                    mode="lines+text",
                    line={'width':0.5, 'color':'blue', 'dash':'dashdot'},
                    name=f"S/R {sr_level}",
                    text=text,
                    textposition="bottom right"
)

        )
        # lines.append(go.Line(
        #
        #     x0=ticker_history[0].dt,
        #     y0=sr_level,
        #     x1=ticker_history[-1].dt,
        #     y1=sr_level, line={'color': 'blue', 'width': 0.25, 'dash':'dashdot'},
        # ))
    return lines


def figures_to_html(ticker,figs):
    # with open(filename, 'w') as dashboard://
    # dashboard = ""
    dashboard = f"<h2>${ticker}</h2>" + "\n"
    for fig in figs:

        inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
        # print(inner_html+"\n\n\n")
        dashboard = dashboard + inner_html+"<br><br>"
    # dashboard.write("</body></html>" + "\n")
    with open("dumb.html", 'w') as f:
        f.write(dashboard)
    return dashboard

def build_indicator_dict(ticker, ticker_history, module_config):
    indicator_dict = {
        "sma": {
            "plot": plot_indicator_data(ticker, ticker_history[-module_config['plot_bars']:],
                                        load_sma(ticker, ticker_history, module_config), module_config,
                                        name='sma10'),
            "overlay": True
        },
        "ema50": {
            "plot": plot_indicator_data(ticker, ticker_history[-module_config['plot_bars']:],
                                        load_golden_cross(ticker, ticker_history, module_config)['sma_short'],
                                        module_config, name='ema50', color='yellow'),
            "overlay": True
        },
        "ema200": {
            "plot": plot_indicator_data(ticker, ticker_history[-module_config['plot_bars']:],
                                        load_golden_cross(ticker, ticker_history, module_config)['sma_long'],
                                        module_config, name='ema200', color='purple'),
            "overlay": True
        },

        "rsi": {
            "plot": plot_indicator_data(ticker, ticker_history[-module_config['plot_bars']:],
                                        load_rsi(ticker, ticker_history, module_config),
                                        module_config, name='rsi', color='Blue'),
            "overlay": False
        },
        "macd": {
            "plot": plot_indicator_data_dual_y_axis(ticker, ticker_history[-module_config['plot_bars']:],
                                                    load_macd(ticker, ticker_history, module_config),
                                                    module_config, keys=['macd', 'signal'], colors=['green', 'red']),
            "overlay": False
        },
        "dmi": {
            "plot": plot_indicator_data_dual_y_axis(ticker, ticker_history[-module_config['plot_bars']:],
                                                    load_dmi_adx(ticker, ticker_history, module_config),
                                                    module_config, keys=['dmi+', 'dmi-', 'adx'],
                                                    colors=['green', 'red', 'blue']),
            "overlay": False
        },
        "s/r levels": {
            "plot": plot_sr_lines(ticker, ticker_history[-module_config['plot_bars']:],
                                  load_support_resistance(ticker, ticker_history, module_config, flatten=True),
                                  module_config),
            "overlay": True
        }

    }

    return indicator_dict