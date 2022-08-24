from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.collection),
    path('list/', views.list),
]