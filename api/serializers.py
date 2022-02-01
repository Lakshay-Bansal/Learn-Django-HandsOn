from rest_framework import serializers
from api import models

class StudentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 100)
    rollNum = serializers.IntegerField()
    marks = serializers.IntegerField()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'
        
class ArticleSerializer(serializers.ModelSerializer):
   # Creating Tag Serializer for the tag in the tag table
   tags = TagSerializer(many = True, read_only = True )

   class Meta:
       model = models.Article
       fields = '__all__'