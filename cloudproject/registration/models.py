from django.db import models

#----------------------------------------------
# User
#----------------------------------------------
class User(models.Model):
    email = models.EmailField(unique=True)
    class RoleChoices(models.TextChoices):
        STUDENT = 'STU', 'Student'
        TEACHER = 'TEA', 'Teacher'
        ADMIN = 'ADM', 'Admin'
    role = models.CharField(max_length=3, choices=RoleChoices.choices, null=True)


#----------------------------------------------
# Faculty and Department
#----------------------------------------------
class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return f"{self.name} ({self.faculty.name})"


#----------------------------------------------
# All Roles
#----------------------------------------------
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    year = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, related_name='students')
    enrolled_courses = models.ManyToManyField('CourseSection', blank=True, related_name='enrolled_students')

    def __str__(self):
        return f"{self.code} - {self.first_name} {self.last_name}"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, related_name='teachers')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


#----------------------------------------------
# Course and Section
#----------------------------------------------
class Course(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    credits = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.code} - {self.name} ({self.department.name})"
    
class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_number = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
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
        unique_together = ('course', 'section_number')

    def __str__(self):
        return f"{self.course.code} ({self.section_number})"


#----------------------------------------------
# Enroll
#----------------------------------------------
class PreEnrollQueue(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_section = models.ForeignKey(CourseSection, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'course_section')
    
    def __str__(self):
        return f"{self.student.student_code} - {self.course_section.course.code} ({self.course_section.section_number})"
