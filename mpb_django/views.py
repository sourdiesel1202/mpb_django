from django.shortcuts import render
import json,os
# Create your views here.
from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db import connection
from datetime import  datetime
from django.template import loader
import traceback

from dashboard.functions import build_dashboard_django


def index(request):
    template = loader.get_template('mpb_django/index.html')
    # reports= Report.objects.all().order_by('name')
    # print(reports)
    # report_schedules ={}
    # for report in reports:
    #     _report_schedules = [x for x in ReportSchedule.objects.filter(report=report)]
    #     if len(_report_schedules) > 0:
    #         report_schedules[report.name]=_report_schedules
    # print(report_schedules)
    timespans = []
    with connection.cursor() as cursor:
        query = """
        select distinct timespan_multiplier, timespan from history_tickerhistory
        """
        cursor.execute(query)
        for row in cursor.fetchall():
            timespans.append({'timespan_multiplier':row[0],'timespan':row[1]})
        # all_count, yes_count = row
    context = {
        "timeframes":timespans
    }
    return HttpResponse(template.render(context, request))


def dashboard(request, timespan_multiplier,timespan):

    #ok here is where we're gonna do the fuckery to load the dashboard, freaking a dude
    #hey dumbass, write the report in sql
    template = loader.get_template('mpb_django/dashboard.html')
    # reports= Report.objects.all().order_by('name')
    # print(reports)
    # report_schedules ={}
    # for report in reports:
    #     _report_schedules = [x for x in ReportSchedule.objects.filter(report=report)]
    #     if len(_report_schedules) > 0:
    #         report_schedules[report.name]=_report_schedules
    # print(report_schedules)
    context = {
        "dashboard_html":build_dashboard_django(connection, timespan, timespan_multiplier)
    }
    return HttpResponse(template.render(context, request))