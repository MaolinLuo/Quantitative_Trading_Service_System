from django.urls import path,include

from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('login/', views.login),
    path('register/', views.register),
    path('toVip/', views.toVip),
    path("stock/", include("Stock.urls")),
    path("strategy/", include("Strategy.urls")),
    path("MarketData/", include("MarketData.urls")),
    path("news/",include("News.urls")),
    path("collection/", include("Collection.urls")),
]