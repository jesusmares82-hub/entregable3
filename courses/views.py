from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from courses.models import Course
from courses.serializers import CourseSerializer


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            permissions = (AllowAny,)
        else:
            permissions = (IsAuthenticated,)

        return [permission() for permission in permissions]
