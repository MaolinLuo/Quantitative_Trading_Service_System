from django.urls import path,include

from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('login/', views.login),
    path('register/', views.register),

    path("stock/", include("Stock.urls")),
    path("UDdistribution/", include("MarketData.urls")),
]