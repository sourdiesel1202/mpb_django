from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:report_id>/get_timeless', views.get_timeless_report, name='get_timeless_report'),
    path('<int:report_id>/get_timeframe', views.get_timeframe_report, name='get_timeframe_report'),
    path('<int:report_id>/get/<str:timespan_multiplier>/<str:timespan>/', views.get_timeframe_report, name='get_report'),
    path('<int:report_id>/getjsreport', views.getjsreport, name='getjsreport'),
    path('<int:report_id>/get_timeframe_reportjs/<str:timespan_multiplier>/<str:timespan>/', views.get_timeframe_reportjs, name='getjsreport'),
    path('<int:report_id>/run', views.run_report, name='run_report'),

]