from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=50)
    roll_no = models.IntegerField(unique=True)
    college = models.ForeignKey('College', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class College(models.Model):
    college_name = models.CharField(max_length=100)

    def __str__(self):
        return self.college_name 