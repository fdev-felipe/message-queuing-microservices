# encoding: utf-8

from django.contrib import admin
from django.urls import path
from api import views as api_views

urlpatterns = [
    path('register', api_views.register, name='user_create'),
    path('login', api_views.login, name='login'),
    path('logout', api_views.logout, name='logout'),
    path('stock', api_views.StockView.as_view(), name='stock'),
    path('history', api_views.HistoryView.as_view(), name='history'),
    path('stats', api_views.StatsView.as_view(), name='stats'),
    path('admin', admin.site.urls),
]
