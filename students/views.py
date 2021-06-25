from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from students.models import Student
from students.serializers import StudentSerializer


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated, )
