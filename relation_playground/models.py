from django.db import models
from django.core.validators import (
    MinValueValidator
)

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey('Author', on_delete= models.CASCADE)
    # If article is deleted then the corresponding author entry in the author table will also get delete

    def __str__(self):
        return self.title

class Author(models.Model):
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# Many-To-Many relationship
class Topping(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(validators=[
        MinValueValidator(0)
    ]) 

    # It will create a many to many mapping with Pizza
    topping = models.ManyToManyField('Topping')
    def __str__(self):
        return self.name
