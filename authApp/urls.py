from django.urls import path
from authApp  import views
from authApp.forms import LoginForm

urlpatterns = [
    # path("", views.login)
    path("login/", views.Login.as_view() ),    # By inbuilt func of Django
    path("logout/", views.Logout.as_view())
]