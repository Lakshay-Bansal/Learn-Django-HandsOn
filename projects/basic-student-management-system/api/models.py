from pyexpat import model
from typing import Type
from django.db import models

# Create your models here.
class Student(models.Model):
    GENDERS = (
        ("f", "female"),
        ("m", "male"),
        ("u", "undisclosed")
    )
    name = models.CharField(max_length=100)
    roll_num = models.IntegerField(unique=True)
    email = models.EmailField(max_length=50)
    gender = models.CharField(max_length=1, choices= GENDERS)
    course = models.CharField(max_length=50)
    attendance = models.IntegerField(default=0)
    institute = models.ForeignKey("Institute", on_delete=models.CASCADE, null = True, blank = True)

    def __str__(self):
        return self.name

class Institute(models.Model):
    TYPES = (
        ("c", "college"),
        ("h", "high school")
    )

    name = models.CharField(max_length=200)
    type_of_institute = models.CharField(max_length=1, choices= TYPES)

    def __str__(self):
        return self.name
