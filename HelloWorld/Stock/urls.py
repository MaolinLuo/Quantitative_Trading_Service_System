from django.urls import path,include

from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('kline/', views.kline),
    path('allStocks/',views.allStocks)
]