from django.contrib import admin
from courses.models import Course, Section, Class

# Register your models here.
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Class)