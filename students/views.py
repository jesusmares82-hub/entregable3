from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from courses.serializers import CourseNameSerializer
from students.models import Student
from students.paginations import CustomPagination
from students.serializers import StudentSerializer


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        send_mail(
            'Welcome to Academlo',
            'Thanks '+request.data['name'],
            'mares@academlo.com',
            [request.data['email']],
            fail_silently=False,
        )
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        data = {}
        for key, value in self.request.query_params.items():
            if key == CustomPagination.page_query_param:
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
    # ManyToManyField actions
    def course(self, request, pk):
        student = self.get_object()

        if request.method == 'GET':
            courses = student.courses.all()
            page = self.paginate_queryset(courses)
            if page:
                serialized = CourseNameSerializer(page, many=True)
                return self.get_paginated_response(serialized.data)

            serialized = CourseNameSerializer(student.courses, many=True)
            return Response(status=status.HTTP_200_OK, data=serialized.data)
