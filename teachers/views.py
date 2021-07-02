from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from teachers.models import Teacher
from teachers.serializers import TeacherSerializer


class TeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    def get_permissions(self):
        print(self.request.method)
        if self.request.method == 'GET':
            permissions = (AllowAny,)
        elif self.request.method == 'DELETE':
            permissions = (IsAdminUser,)
        else:
            permissions = (IsAuthenticated,)

        return [permission() for permission in permissions]


