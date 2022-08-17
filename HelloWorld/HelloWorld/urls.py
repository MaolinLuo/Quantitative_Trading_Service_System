from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login),
    # path('register/', views.register),
    # path('rb1/', views.rb1),
    # path('rb2/', views.rb2),
    # path('search/', search.search),
    # path('search_form/', search.search_form),
    # path('testdb/', testdb.testdb),
]