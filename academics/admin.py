from django.contrib import admin
from .models import *

# Register your models here.
class FacultyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Faculty, FacultyAdmin)
