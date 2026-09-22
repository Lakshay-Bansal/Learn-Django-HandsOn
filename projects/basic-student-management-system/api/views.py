from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    ListCreateAPIView,
    DestroyAPIView
) 

from api import models, serializers
# Create your views here.
class StudentListView(ListAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializers

class StudentDetailView(RetrieveAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializers

# By sending the delete request from Postman at that url page of student
class StudentDeleteView(DestroyAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializers

