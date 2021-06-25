from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from students.models import Student
from students.serializers import StudentSerializer


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            permissions = (AllowAny, )
        else:
            permissions = (IsAuthenticated, )

        return [permission() for permission in permissions]
