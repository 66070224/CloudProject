from django.db import models

class PreEnrollQueue(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    course_section = models.ForeignKey("academics.CourseSection", on_delete=models.CASCADE)

    class Meta:       
        constraints = [
            models.UniqueConstraint(fields=['student', 'course_section'], name='unique_student_course_section')
        ]
    
    def __str__(self):
        return f"{self.student.code} - {self.course_section.course.code} ({self.course_section.section_number})"

class EnrollStudent(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    course_section = models.ForeignKey("academics.CourseSection", on_delete=models.CASCADE)
    class GradeChoices(models.TextChoices):
        A = 'A', 'A'
        B_PLUS = 'B+', 'B+'
        C_PLUS = 'C+', 'C+'
        D_PLUS = 'D+', 'D+'
        B = 'B', 'B'
        C = 'C', 'C'
        D = 'D', 'D'
        F = 'F', 'F'
    grade = models.CharField(max_length=3, choices=GradeChoices.choices)

    def __str__(self):
        return f"Grade : {self.grade}"