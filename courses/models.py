from django.db import models
from django.contrib.auth.models import User
from students.models import Student
from teachers.models import Teacher


class Course(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.CharField(max_length=50)
    course_days = models.CharField(max_length=50)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    # ForeignKey, a course has only one teacher, but the same teacher can have many courses.
    students = models.ManyToManyField(Student, related_name='courses')
    # ManyToManyField, a course can have many students and a student can have multiple courses.

    def __str__(self):
        return self.name
