from django.db import models

from accounts.models import CustomUser
from departments.models import Department, Faculty
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name="student")
    student_id = models.CharField(max_length=8, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.IntegerField()
    enrolled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student_id} {self.user.first_name}"

class Professor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name="professor")
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.department} {self.user.first_name}"

class Registra(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name="registra")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.faculty} {self.user.first_name}"
    
class Payment(models.Model):
    student = models.ForeignKey(Student, related_name="payments", on_delete=models.CASCADE)
    department = department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="payments")
    year = models.IntegerField()
    term = models.IntegerField()
    class StatusChoices(models.TextChoices):
        NO = "N", _("ยัง")
        WAIT = "W", _("รอตรวจสอบ")
        YES = "Y", _("ยืนยัน")
    pay = models.CharField(max_length=1, choices=StatusChoices, default=StatusChoices.NO)
    slip = models.ImageField(upload_to="slips/", blank=True, null=True)
    