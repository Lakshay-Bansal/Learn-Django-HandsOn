from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, 'main/index.html')

def sshh(request):
    return HttpResponse("This is the Authenticator Hands On")