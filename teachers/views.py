from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from teachers.models import Teacher
from teachers.serializers import TeacherSerializer


class TeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    pagination_class = None

    def get_queryset(self):
        data = {}
        for key, value in self.request.query_params.items():
            if not key == 'name':
                continue
            data[key] = value
        return self.queryset.filter(**data)

    def get_permissions(self):
        if self.request.method == 'GET':
            permissions = (AllowAny,)
        elif self.request.method == 'DELETE':
            permissions = (IsAdminUser,)
        else:
            permissions = (IsAuthenticated,)

        return [permission() for permission in permissions]






