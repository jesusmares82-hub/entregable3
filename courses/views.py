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


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = (CoursePermissions, )

    def get_queryset(self):
        print('Entry')
        data = {}
        for key, value in self.request.query_params.items():
            if not key == 'name':
                continue
            data[key] = value
        return self.queryset.filter(**data)

    @action(methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'], detail=True)
    # ManyToManyField actions
    def student(self, request, pk):
        course = self.get_object()

        if request.method == 'GET':
            serialized = StudentCourseSerializer(course.students, many=True)
            return Response(status=status.HTTP_200_OK, data=serialized.data)

        if request.method in ['POST', 'PUT', 'PATCH']:
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
