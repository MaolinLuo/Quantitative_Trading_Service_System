from django.urls import path,include

from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('list/', views.list),
    path('sma/', views.sma),
    path('turtle/', views.turtle),
]