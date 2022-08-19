from django.urls import path,include

from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('login/', views.login),
    path('register/', views.register),

    path("stock/", include("Stock.urls")),
<<<<<<< HEAD
    path("strategy/", include("Strategy.urls")),
=======
    path("UDdistribution/", include("MarketData.urls")),
>>>>>>> c51ca6964c26720b9e21a89faad614daf23b30f2
]