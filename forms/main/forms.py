from django import forms
from main import models

class ExampleForm(forms.Form):
    name = forms.CharField(max_length=50)
    about_me = forms.CharField(widget= forms.Textarea())
    active = forms.BooleanField()

# As we mostly require to fill the data from front end to our backend created fields
# There is a option to create forms directly for those DDL
class StudentForm(forms.ModelForm):
    class Meta:
        model = models.Student  #Student is the class created in main/models.py 
        fields = '__all__'
