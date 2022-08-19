from django.urls import path,include

from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('login/', views.login),
    path('register/', views.register),
    path("stock/", include("Stock.urls")),
    path("strategy/", include("Strategy.urls")),
    path("MarketData/", include("MarketData.urls")),
]