from re import template
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# Create your views here.

# def index(request):
#     context = {

#     }
#     return render(request, 'main/index.html', context)
# Rather then defining function now we use inbuilt class of View in Django

class Index(View):
    def get(self, request):
        return HttpResponse("GET Request! Working Fine")
    
    def post(self, request):
        return HttpResponse("POST Request")

# Django provide us with five views
# 1. Detail View
# 2. List View
# 3. Create View
# 4. Update View
# 5. Delete View

from django.views import View
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from main import models

class CollegeDetail(DetailView):
    model = models.College
    template_name = 'main/college_detail.html'

class CollegeList(ListView):
    model = models.College
    template_name = 'main/college_list.html'
    context_object_name = 'colleges' 

class CollegeCreate(CreateView):
    model = models.College
    template_name = 'main/create_college.html'
    fields = '__all__'
    success_url = '/college'   # At which after form submission the submit direct the page to 

class StudentCreate(CreateView):
    model = models.Student
    template_name = 'main/create_student.html'
    fields = '__all__'
    success_url = '/create_student'

class CollegeUpdate(UpdateView):
    model = models.College
    template_name = 'main/create_college.html'
    fields = '__all__'
    success_url = '/college'

class StudentDelete(DeleteView):
    model = models.Student
    template_name = 'main/confirm.html'
    success_url =  '/'