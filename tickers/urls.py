from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ticker/<str:timespan_multiplier>/<str:timespan>/<str:ticker>/chart/', views.view_ticker_chart),
    path('contract/<str:timespan_multiplier>/<str:timespan>/<str:contract>/chart/', views.view_contract_chart),

]