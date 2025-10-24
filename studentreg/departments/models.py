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
    
class Semester(models.Model):
    year = models.IntegerField()
    term = models.IntegerField()

    def __str__(self):
        return f"{self.year} {self.term}"
