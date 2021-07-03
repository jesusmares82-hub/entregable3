from rest_framework.serializers import ModelSerializer

from students.models import Student


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class StudentUserSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class StudentCourseSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', )
