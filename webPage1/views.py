from urllib import response
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # response = HttpResponse("Welcome to the first webpage of Django")   #This will not create the html page for the code
    developed_by = "Dynamic Feature"
    friends = [
        "Lakshay Bansal",
        "Shubham Bhati",
        "Shivam",
        "Manish Yadav"
    ]
    message = "Now using dyamic feature call"

    context = {
        "developer":developed_by,
        "friends": friends,
        "heading": message
    }

    response = render(request, 'webPage1/index.html', context)
    return response

def wp2(request):
    response = render(request, "webPage1/index_wp2.html")
    return response
