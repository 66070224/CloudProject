from django.db import models
from django.contrib.auth.models import User as AuthUser

#----------------------------------------------
# User
#----------------------------------------------
class UserInfo(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(unique=True)
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    class RoleChoices(models.TextChoices):
        STUDENT = 'STU', 'Student'
        TEACHER = 'TEA', 'Teacher'
    role = models.CharField(max_length=3, choices=RoleChoices.choices)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

#----------------------------------------------
# Faculty and Department
#----------------------------------------------
class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return f"{self.name} ({self.faculty.name})"


#----------------------------------------------
# All Roles
#----------------------------------------------
class Student(models.Model):
    from_user = models.OneToOneField(UserInfo, on_delete=models.CASCADE, primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    year = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, related_name='students')
    enrolled_courses = models.ManyToManyField('CourseSection', blank=True, related_name='enrolled_students')

    def __str__(self):
        return f"{self.code} - {self.from_user.first_name} {self.from_user.last_name}"

class Teacher(models.Model):
    from_user = models.OneToOneField(UserInfo, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, related_name='teachers')

    def __str__(self):
        return f"{self.from_user.first_name} {self.from_user.last_name}"


#----------------------------------------------
# Course and Section
#----------------------------------------------
class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    credits = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    teachers = models.ManyToManyField(Teacher, related_name="courses")

    def __str__(self):
        return f"{self.code} - {self.name} ({self.department.name})"
    
class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_sections')
    section_number = models.IntegerField()
    capacity = models.IntegerField()
    class Meta:
        unique_together = ('course', 'section_number')

    def __str__(self):
        return f"{self.course.code} {self.course.name} - Section {self.section_number}"
    
class SectionClass(models.Model):
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name='section_class')
    class TypeChoices(models.TextChoices):
        LECTURE = 'LEC', 'Lecture'
        LAB = 'LAB', 'Lab'
    class_type = models.CharField(max_length=3, choices=TypeChoices.choices)
    class DayChoices(models.TextChoices):
        SUNDAY = 'Sun', 'Sunday'
        MONDAY = 'Mon', 'Monday'
        TUESDAY = 'Tue', 'Tuesday'
        WEDNESDAY = 'Wed', 'Wednesday'
        THURSDAY = 'Thu', 'Thursday'
        FRIDAY = 'Fri', 'Friday'
        SATURDAY = 'Sat', 'Saturday'
    day = models.CharField(max_length=3, choices=DayChoices.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.section.course.code} - Section {self.section.section_number}: {self.day} {self.start_time}-{self.end_time}"


#----------------------------------------------
# Enroll
#----------------------------------------------
class EnrollQueue(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enroll_queues')
    course_section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name='enroll_queues')
    enroll_time = models.DateTimeField(auto_created=True)

    class Meta:
        unique_together = ('student', 'course_section')
    
    def __str__(self):
        return f"{self.student.code} - {self.course_section.course.name}:{self.course_section.section_number} - {self.enroll_time}"
