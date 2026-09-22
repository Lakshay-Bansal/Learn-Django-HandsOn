from django.contrib import admin
from relation_playground import models

# Register your models here.

admin.site.register([
    models.Article,
    models.Author,
    models.Pizza,
    models.Topping
])

