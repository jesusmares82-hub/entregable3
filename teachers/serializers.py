from rest_framework.serializers import ModelSerializer

from teachers.models import Teacher


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherCourseSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'name', 'email')
