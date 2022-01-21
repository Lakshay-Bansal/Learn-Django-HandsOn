from django.contrib import admin
from main import models

# Register your models here.

admin.site.register([
    models.Student  # As inside main/models.py we had created a class Student that we want to register
])
 