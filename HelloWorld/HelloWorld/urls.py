from django.urls import path,include

from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('login/', views.login),
    path('register/', views.register),
    path("stock/", include("Stock.urls")),
    path("strategy/", include("Strategy.urls")),
<<<<<<< HEAD
    path("UDdistribution/", include("MarketData.urls")),
=======
>>>>>>> b1d80099ade3d7f3f525d495fb4b7e3c7cec8f76
]