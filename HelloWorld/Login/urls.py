from django.urls import path

from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('runoob/', views.runoob),
    path('rb1/', views.rb1),
    path('rb2/', views.rb2),
    path('search/', search.search),
    path('search_form/', search.search_form),
    path('testdb/', testdb.testdb),
]
