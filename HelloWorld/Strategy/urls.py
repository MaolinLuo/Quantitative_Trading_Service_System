from django.urls import path,include

from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('list/', views.list),
    path('sma/', views.sma),
    path('turtle/', views.turtle),
    path('gru/', views.gru),
    path('keltner/', views.keltner),
    path('boll/', views.boll),
    path('mfi/', views.mfi),
    path('rnn/', views.rnn),
    path('lstm/', views.lstm),
    path('uploadCode/', views.uploadCode),
    path('downloadCode/', views.downloadCode),
]