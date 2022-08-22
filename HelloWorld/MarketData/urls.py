from django.urls import path,include

from . import views

urlpatterns = [
    path('UDdistribution/', views.UDdistribution),
    path('StockIndex/', views.StockIndex),
    path('MostPopular/', views.MostPopular),
]