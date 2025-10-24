from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta

from departments.models import Department
from personnels.models import Professor

# Create your models here.
class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    credits = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    professors = models.ManyToManyField(Professor, related_name="courses")
    year = models.IntegerField(blank=True)
    term = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.name}"

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
    number = models.IntegerField()
    capacity = models.IntegerField()

    class Meta:
        unique_together = ('course', 'number')

    def __str__(self):
        return f"{self.course.name} {self.number}"

class Class(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='classes')
    class TypeChoices(models.TextChoices):
        LECTURE = 'LEC', _('Lecture')
        LAB = 'LAB', _('Lab')
    type = models.CharField(max_length=3, choices=TypeChoices.choices)
    class DayChoices(models.TextChoices):
        MONDAY = 'Mon', _('Monday')
        TUESDAY = 'Tue', _('Tuesday')
        WEDNESDAY = 'Wed', _('Wednesday')
        THURSDAY = 'Thu', _('Thursday')
        FRIDAY = 'Fri', _('Friday')
        SATURDAY = 'Sat', _('Saturday')
        SUNDAY = 'Sun', _('Sunday')
    day = models.CharField(max_length=3, choices=DayChoices.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)

    @property
    def duration(self):
        start = datetime.combine(datetime.today(), self.start_time)
        end = datetime.combine(datetime.today(), self.end_time)
        return int((end - start).total_seconds() / 60)
    
    def __str__(self):
        return f"{self.section} {self.type}"