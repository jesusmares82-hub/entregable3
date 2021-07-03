from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from courses.permissions import CoursePermissions
from students.models import Student
from teachers.models import Teacher
from courses.models import Course
from rest_framework.viewsets import ModelViewSet
from courses.serializers import CourseSerializer
from students.serializers import StudentCourseSerializer
from teachers.serializers import TeacherCourseSerializer
from django.core.mail import send_mail


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = (CoursePermissions, )

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        send_mail(
            'A new course was added to the system',
            'Thanks for adding a new course!',
            'mares@acxademlo.com',
            [request.user.email],
            fail_silently=False,
        )
        serializer = self.get_serializer_class()
        serialized = serializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(status=status.HTTP_201_CREATED, data=serialized.data)

    def get_queryset(self):
        data = {}
        for key, value in self.request.query_params.items():
            if key == 'page':
                continue
            data[key] = value
        return self.queryset.filter(**data)

    @action(methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'], detail=True)
    # ManyToManyField actions
    def student(self, request, pk):
        course = self.get_object()

        if request.method == 'GET':
            students = course.students.all()
            page = self.paginate_queryset(students)
            if page:
                serialized = StudentCourseSerializer(page, many=True)
                return self.get_paginated_response(serialized.data)

            serialized = StudentCourseSerializer(course.students, many=True)
            return Response(status=status.HTTP_200_OK, data=serialized.data)

        if request.method in ['POST', 'PUT', 'PATCH']:
            students = Student.objects.filter(id__in=request.data['students'])
            for student in students:
                send_mail(
                    'A new course was added.',
                    'Welcome to the new course!',
                    'mares@acxademlo.com',
                    [student.email],
                    fail_silently=False,
                )
            course.students.set(Student.objects.filter(id__in=request.data['students']))
            return Response(status=status.HTTP_200_OK)

        if request.method == 'DELETE':
            student_ids_delete = request.data['students']
            for student_id in student_ids_delete:
                student = Student.objects.get(id=student_id)
                course.students.remove(student)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'], detail=True)
    # ForeignKey actions
    def teacher(self, request, pk):
        course = self.get_object()

        if request.method == 'GET':
            serialized = TeacherCourseSerializer(course.teacher)
            return Response(status=status.HTTP_200_OK, data=serialized.data)

        if request.method in ['POST', 'PUT', 'PATCH']:
            teacher = Teacher.objects.get(id=request.data['teacher'])
            course.teacher = teacher
            course.save()
            return Response(status=status.HTTP_200_OK)

        if request.method == 'DELETE':
            course.teacher = None
            course.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
