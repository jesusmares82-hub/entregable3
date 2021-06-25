from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from courses.models import Course
from courses.serializers import CourseSerializer


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        print(self.request.method)
        if self.request.method == 'GET':
            permissions = (AllowAny,)
        elif self.request.method == 'DELETE':
            permissions = (IsAdminUser,)
        else:
            permissions = (IsAuthenticated,)

        return [permission() for permission in permissions]
