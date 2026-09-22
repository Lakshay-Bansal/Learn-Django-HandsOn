from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import HttpResponse
import json

from api import serializers, models

# Create your views here.

# Now we will create the views using nbuilt django views
from rest_framework.parsers import JSONParser
from rest_framework.generics import (
    ListAPIView, 
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    ListCreateAPIView
)


class ArticleListView(ListAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer

class ArticleDetailView(RetrieveAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer

# This will update the article content for the Patch request 
# received via a webpage for the existing article in db
class ArticleDetailView(RetrieveUpdateAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer

# To create a new article
class ArticleListView(ListCreateAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer

"""
@api_view()
def articleApi(request):
    articles = models.Article.objects.all()
    response = serializers.ArticleSerializer(articles, many = True)
    return Response(response.data)


@api_view(['POST', 'GET'])
def createArticleApi(request):
    # # Get data from webpage and post back to wepage
    # print(request.body)
    # return Response(request.body)
    # return Response({"message": "Welcome to Create your Article"})
    
    # # To get the data as json formated use
    # body = json.loads(request.body)
    # return Response(body)

    # To save the data received from webpage to a db of django table
    body = json.loads(request.body)
    response = serializers.ArticleSerializer(data = body)

    if response.is_valid():
        inst = response.save()
        response = serializers.ArticleSerializer(inst)
        return Response(response.data)
    
    return Response(response.errors)

"""




## It will return the json data to website
# @api_view(('GET',))
# def usersAPI(request):
#     users = [
#         {
#             "name": "Lakshay",
#             "city": "Faridabad"
#         },
#         {
#             "name": "Shubham",
#             "city": "Jewar"
#         },
#         {
#             "name": "Mohit",
#             "city": "Delhi"
#         }
#     ]
#     return Response(users)



# from django.http import HttpResponse
# import json

# def usersAPI(request):
#     users = [
#         {
#             "name": "Lakshay",
#             "city": "Faridabad"
#         },
#         {
#             "name": "Shubham",
#             "city": "Jewar"
#         },
#         {
#             "name": "Mohit",
#             "city": "Delhi"
#         }
#     ]
#    #   It will  treat the data send as the HTML
#     return HttpResponse(users)
#     # It will make the data to be treated as string
#     return HttpResponse(json.dumps(users))



#  # Basics of sending data in a class
# class Student:
#     def __init__(self, name, rollNum, marks):
#         self.name = name
#         self.rollNum = rollNum
#         self.marks = marks

# @api_view()
# def usersAPI(request):
#     std1 = Student("Lakshay", 56, 100)
#     std2 = Student("Ram", 86, 120)
#     std3 = Student("Shivam", 13, 98)
#     response = serializers.StudentSerializer([
#         std1,
#         std2,
#         std3
#     ], many = True)
#     return Response(response.data)