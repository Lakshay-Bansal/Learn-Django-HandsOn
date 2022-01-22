from django.shortcuts import render
from django.http import HttpResponseRedirect
from main import (
    forms,
    models
)

# Create your views here.

#We can take input directly from the user 
# By passing the form class to the html page
def index(request):
    context = {
        "form": forms.ExampleForm
    }
    return render(request, 'main/index.html', context)

# This will show the store student data in database
def student_data(request):
    students = models.Student.objects.all()
    context = {
        "students": students
    }
    return render(request, 'main/student_data.html', context)

# It will create a form to get data from the user to add it in exiting daatbase
def add_student(request):
    studentForm = forms.StudentForm()

    if request.method == 'POST':
        studentForm = forms.StudentForm(request.POST)
        if studentForm.is_valid():
            students = studentForm.save()
            return HttpResponseRedirect('/student')


    context={
        "studentForm": studentForm
    }
    return render(request, 'main/add_student.html', context)