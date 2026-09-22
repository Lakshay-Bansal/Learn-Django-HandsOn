from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('student', views.student_data, name='student_data'),
    path('add_student', views.add_student, name= 'add_student')
]