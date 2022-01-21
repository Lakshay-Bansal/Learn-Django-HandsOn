from django.db import models

from django.core.validators import (
    EmailValidator,
    MaxValueValidator,
    MinValueValidator,
    URLValidator,
    validate_slug
)

from main.validators import (
    validate_even_number # Which is a function define in validator class
)
# Create your models here.

# evry table in database is represented as a class
# every row in database is represented by an object of this class
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.IntegerField()
    course = models.CharField(max_length=6)    # As BTech or MTech
    branch = models.CharField(max_length=30)   # As Electronics, CS, CSP, VLSI, etc.

    # Different data fields in Djnago for SQL
    GENDERS = (
        ('f', 'Female'),
        ('m', 'Male'),
        ('u', 'Undisclosed')
    )
    # Textfiled we doesn't require to specify the length as in char field
    address = models.TextField(null = True)
    
    """
    # By default all the fields are not null in Djnago
    # We need to explicity define that they can be null in database
    # But user left the blank field then form mdoesn't accept it because of ORM
    # That's why we need to define blank = True also
    """
    # EmailField validate the correctness of mail id
    email = models.EmailField(null = True, blank = True)
    #Define email as the charfield and explictly providing the validators
    email = models.CharField(
        max_length=50, 
        validators=[EmailValidator(message="Please check your email again")],
        null=True 
    )

    gender = models.CharField(max_length=1, choices=GENDERS, null=True)

    age = models.IntegerField(
        null = True,
        validators= [ 
            MaxValueValidator(150), 
            MinValueValidator(0),
            validate_even_number ]
    )

    # slug contain in the url of the website
    #They can contain char, numerals, - and _ only
    slug = models.CharField(max_length=150, validators=[validate_slug], null=True)
    
    
    """
    As we had seen on admin page it shows as Student object(1)
    To override this we use the dunder method of class
    """
    def __str__(self):
        return self.name

