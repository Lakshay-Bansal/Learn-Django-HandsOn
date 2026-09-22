from django.urls import path
from main import views

urlpatterns = [
    path('projects/', views.projects, name = "projects"),
    path('hobby/', views.hobby, name = "hobby"),

    path('', views.index, name = "index")
]