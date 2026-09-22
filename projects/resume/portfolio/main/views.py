from urllib import request
from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}
    return render(request, 'main/index.html', context)

def projects(request):
    context = {}
    return render(request, 'main/projects.html', context)

def hobby(request):
    context = {}
    return render(request, 'main/hobby.html', context)