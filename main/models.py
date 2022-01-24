from turtle import ondrag
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    slug = models.SlugField()
    content = models.CharField(max_length=1024)

    def __str__(self):
        return self.content

class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    choice = models.ForeignKey('Choice', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.user, self.choice)

class Choice(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    content = models.CharField(max_length= 256)

    def __str__(self):
        return "{} - {}".format(self.question.content[:100], self.content)

    def answer_count(self) :
        count = Answer.objects.filter(
            question = self.question,
            choice = self.id 
        ).count()

        return count