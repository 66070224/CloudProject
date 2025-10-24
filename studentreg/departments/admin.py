from django.contrib import admin
from departments.models import Faculty, Department, Semester

# Register your models here.
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Semester)