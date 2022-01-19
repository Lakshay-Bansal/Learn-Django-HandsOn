from django.urls import path

from webPage1 import views

urlpatterns = [
    path('', views.index),
    path('wp2/', views.wp2)
]