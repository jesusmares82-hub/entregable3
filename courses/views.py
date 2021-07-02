from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from students.models import Student
from rest_framework.viewsets import ModelViewSet

from courses.models import Course
from courses.serializers import CourseSerializer
from students.serializers import StudentCourseSerializer


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_queryset(self):
        print('Entry')
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

    @action(methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'], detail=True)
    def student(self, request, pk):
        course = self.get_object()

        if request.method == 'GET':
            serialized = StudentCourseSerializer(course.students, many=True)
            return Response(status=status.HTTP_200_OK, data=serialized.data)

        if request.method in ['POST', 'PUT', 'PATCH']:
            course.students.set(Student.objects.filter(id__in=request.data['students']))
            course.save()
            return Response(status=status.HTTP_200_OK)

        if request.method == 'DELETE':
            course.students.set([])
            course.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
