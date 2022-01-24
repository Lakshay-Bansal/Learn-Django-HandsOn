from django.urls import path

from main import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('home/', views.Index.as_view(), name = 'index'),
    # path('question/<int:pk>', views.Question.as_view(), name='question'),
    # Using slug which is same to the question is the best way
    path('question/<slug>', login_required(views.Question.as_view()), name='question'),
]