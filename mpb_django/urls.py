"""mpb_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mpb_django import views
urlpatterns = [
    path('', views.index),
    path('<str:timespan_multiplier>/<str:timespan>/dashboard', views.dashboard),
    path('admin/', admin.site.urls),
    path('tickers/', include('tickers.urls')),
    # path('<int:report_id>/get', views.get_report, name='get_report'),
    # path('<int:report_id>/view_history', views.view_history, name='view_history'),
    # path('<int:report_id>/view_actions', views.view_actions, name='view_actions'),
    # p
]
