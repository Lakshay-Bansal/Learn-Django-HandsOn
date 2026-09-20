from xml.parsers.expat import model
from django.db import models

# Create your models here.
class Student(models.Model):
    Genders = (
        ('F', 'Female'),
        ('M', 'Male')
    )
    name = models.CharField(max_length=100)
    roll_no = models.IntegerField()
    gender = models.CharField(max_length=1, choices=Genders)

    def __str__(self):
        return self.name