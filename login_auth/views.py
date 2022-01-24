from django.shortcuts import render
from django.contrib.auth.views import (
    LoginView, 
    LogoutView as Logout
)

# Create your views here.
class Login(LoginView):
    template_name = 'login_auth/login.html'
    redirect_authenticated_user = True
    allow_authenticate_user = False