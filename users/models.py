from django.db import models

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, max_length=254)
    code = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    year = models.IntegerField(default=1)
    department = models.ForeignKey("academics.Department", on_delete=models.CASCADE, null=True)
    enrolled_courses = models.ManyToManyField('academics.CourseSection', blank=True, through="enrollment.EnrollStudent")

    def __str__(self):
        return f"{self.code} - {self.first_name} {self.last_name}"