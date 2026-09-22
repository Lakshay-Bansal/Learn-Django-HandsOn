from django.shortcuts import render
from authApp import forms
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect

# Create your views here.
def login(request):
    loginForm =  forms.LoginForm()
    error = None
    
    if request.method == "POST":
        loginForm = forms.LoginForm(request.POST)
        if loginForm.is_valid():
            # print(loginForm) For debug purpose
            name = loginForm.cleaned_data['username'] 
            pasw = loginForm.cleaned_data['password']
            user = authenticate(username = name, password = pasw)
            if user:
                ## Before opening the page it authenticate the user
                auth_login(request, user)
                return HttpResponseRedirect('/')
            else:
                error = "Invalid username or password"
            
    context = {
        "form": loginForm,
        "error": error
    } 

    return render(request, 'authApp/login.html', context)


## Now we write the whole login using inbuilt functions in Django
from django.contrib.auth.views import LoginView, LogoutView

class Login(LoginView):
    template_name = 'authApp/login.html'
    redirect_authenticate_user = True

class Logout(LogoutView):
    pass