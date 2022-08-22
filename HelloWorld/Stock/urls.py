from django.urls import path,include

from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('kline/', views.kline),
    path('allStocks/',views.allStocks),
    path('realTableData/',views.realTableData),
    path('realBaseData/', views.realBaseData),
    path('companyinfo/', views.companyinfo),
]