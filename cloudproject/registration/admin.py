from django.contrib import admin

from .models import *

admin.site.register(UserInfo)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(CourseSection)