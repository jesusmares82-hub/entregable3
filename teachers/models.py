from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField()
    dob = models.DateField()

    def __str__(self):
        return self.name
