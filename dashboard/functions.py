import json
from dashboard.strings import dashboard_template
from mpb_django.functions import execute_query, timestamp_to_datetime, human_readable_datetime


def build_tabulator_basic_data(input_data):
    data = []
    report_attrs = input_data
    # print(report_attrs[0])
    for i in range(1, len(report_attrs)):
        entry = {}
        for ii in range(0, len(report_attrs[i])):
            entry[report_attrs[0][ii]]=report_attrs[i][ii]
        data.append(entry)
    return data


def build_dashboard_django(connection, timespan, timespan_multiplier):
    query=f"""select distinct  th.timestamp, t.symbol, th.close,th.volume, group_concat(distinct tv.position_type separator  ',') positions_validated, count(distinct ta.alert_type) pick_level,group_concat(distinct ta.alert_type separator  ',') alerts_triggered,group_concat(distinct tlt.symbol separator  ',') similar_ticker_lines, group_concat(distinct tbv.position_type separator  ',') backtested_positions  from history_tickerhistory th , tickers_ticker t, validation_tickervalidation tv, alerts_tickeralert ta, lines_similarline tl, tickers_ticker tlt, backtests_backtest tb, validation_tickervalidation tbv where tbv.id=tb.validation_id and tb.validation_id=tv.id and tl.ticker_history_id =th.id and tl.ticker_id=tlt.id and  ta.ticker_history_id=th.id and tv.ticker_history_id=th.id and t.id=th.ticker_id and th.timestamp= (select max(timestamp) from history_tickerhistory where timespan_multiplier='{timespan_multiplier}' and timespan='{timespan}') and th.timespan_multiplier='{timespan_multiplier}' and th.timespan='{timespan}' group by th.id, th.timestamp, t.symbol, th.close,th.volume"""
    # results =
    return build_dashboard(execute_query(connection, query), timespan,timespan_multiplier)
    # with connection.cursor() as cursor:
    #     query = """
    #     select distinct timespan_multiplier, timespan from history_tickerhistory
    #     """
    #     cursor.execute(query)
    #     for row in cursor.fetchall():
    #         timespans.append({'timespan_multiplier':row[0],'timespan':row[1]})
    # pass
def build_dashboard(mpb_data, timespan, timespan_multiplier):
    # with open('html/head.html') as f:
    #     raw_html = f.read()

    # mpb_data = read_csv("mpb.csv")
    # [x.split(".csv")[0] for x in os.listdir(f"{module_config['output_dir']}cached/")]
    date_string = max([human_readable_datetime(timestamp_to_datetime(int(x[0]))) for x in mpb_data[1:]])
    type = f"{timespan_multiplier} "+timespan[0].upper()+timespan[1:]
    for i in range(1, len(mpb_data)):
        # print(f"{human_readable_datetime(timestamp_to_datetime(mpb_data[i][0]))}")
        mpb_data[i][0]=human_readable_datetime(timestamp_to_datetime(mpb_data[i][0]))
    tabulator_data = build_tabulator_basic_data(mpb_data)
    return dashboard_template.replace("//replace_me_with_output", f"var tabledata = {json.dumps(tabulator_data)}").replace("{{report.name}}", f"MPB Traders Report<br>{type}<br>{date_string.split(' ')[0]}<br>{date_string.split(' ')[1]}<br>")
