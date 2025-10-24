from django.db import models
from django.utils.translation import gettext_lazy as _

from personnels.models import Student
from courses.models import Section

# Create your models here.
class Enroll(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrolls")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="enrolls")
    date = models.DateTimeField(auto_now=True)
    class StatusChoices(models.TextChoices):
        PENDING = "pen", _("Pending")
        CONFIRM = "con", _("Confirm")
    status = models.CharField(max_length=3, choices=StatusChoices.choices, default=StatusChoices.PENDING)

    class Meta():
        unique_together = ('student', 'section')
