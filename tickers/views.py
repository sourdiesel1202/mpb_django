from django.shortcuts import render
import json,os
# Create your views here.
from django.utils import timezone

# from .functions import random_color, run_report as run_report_task, build_chartjs_line_data, build_chartjs_bar_data, build_chartjs_pie_data,build_tabulator_basic_data
# from .models import Report, ReportHistory, ReportSchedule, ReportAction, ReportActionHistory
# from config.models import Connection
# from config.classes import OracleConnector
# from config.encryption import encrypt_message, decrypt_message
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from datetime import  datetime
from django.template import loader
# from .classes import  Workbook
# from django.contrib import messages
# from django.http import FileResponse
import traceback
# from mpb_django.decorators  import requires_password_reset
# @requires_password_reset
def index(request):
    template = loader.get_template('reports/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))