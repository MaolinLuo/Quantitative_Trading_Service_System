from django.urls import path,include

from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('list/', views.list),
]