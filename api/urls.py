from django.urls import path
from api import views

urlpatterns = [
    path("std/", views.StudentListView.as_view()),
    path("std/<int:pk>", views.StudentDetailView.as_view()),
    path("deleteStd/<int:pk>", views.StudentDeleteView.as_view())
]