from django.db import models

from accounts.models import CustomUser
from departments.models import Department, Faculty

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    student_id = models.CharField(max_length=8, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.student_id} {self.user.first_name}"

class Professor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.department} {self.user.first_name}"

class Registra(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.faculty} {self.user.first_name}"
    