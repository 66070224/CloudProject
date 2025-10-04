from django.db import models

# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    term_fees = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.faculty.name})"
    
class Professor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Course(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    credits = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} - {self.name} ({self.department.name})"
    
class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_number = models.IntegerField()
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    class TypeChoices(models.TextChoices):
        LECTURE = 'LEC', 'Lecture'
        LAB = 'LAB', 'Lab'
    class_type = models.CharField(max_length=3, choices=TypeChoices.choices)
    class DayChoices(models.TextChoices):
        MONDAY = 'Mon', 'Monday'
        TUESDAY = 'Tue', 'Tuesday'
        WEDNESDAY = 'Wed', 'Wednesday'
        THURSDAY = 'Thu', 'Thursday'
        FRIDAY = 'Fri', 'Friday'
        SATURDAY = 'Sat', 'Saturday'
        SUNDAY = 'Sun', 'Sunday'
    day = models.CharField(max_length=3, choices=DayChoices.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'section_number'], name='unique_course_section')
        ]

    def __str__(self):
        return f"{self.course.code} - Section {self.section_number}"