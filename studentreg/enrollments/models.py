from django.db import models
from django.utils.translation import gettext_lazy as _

from personnels.models import Student
from courses.models import Section, Course

# Create your models here.
class Enroll(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrolls")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrolls")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="enrolls")
    date = models.DateTimeField(auto_now=True)
    class StatusChoices(models.TextChoices):
        PENDING = "pen", _("Pending")
        CONFIRM = "con", _("Confirm")
    status = models.CharField(max_length=3, choices=StatusChoices.choices, default=StatusChoices.PENDING)

    class Meta():
        unique_together = ('student', 'course')

class Grade(models.Model):
    enroll = models.OneToOneField(Enroll, on_delete=models.CASCADE, primary_key=True, related_name="grade")
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    score3 = models.IntegerField(default=0)
    score4 = models.IntegerField(default=0)

    @property
    def get_finalscore(self):
        return self.score1 + self.score2 + self.score2 + self.score3

