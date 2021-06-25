from django.db import models

from students.models import Student


class Course(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.CharField(max_length=50)
    course_days = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    students = models.ManyToManyField(Student, related_name='courses')

    def __str__(self):
        return self.name
