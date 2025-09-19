from django.views import View
from django.shortcuts import render, redirect
from ..models import *
from django.db.models import OuterRef
from django.db.models import F

class RegistrationView(View):

    def get(self, request):
        student = request.session.pop("user", None)
        courses = Course.objects.filter(department=student.department).prefetch_related('course_sections')
        data = []
        for course in courses:
            data.append({
                "code": course.code,
                "name": course.name,
                "credits": course.credits,
                "teachers": [
                    {
                        "title": teacher.from_user.title,
                        "first_name": teacher.from_user.first_name,
                        "last_name": teacher.from_user.last_name,
                    }
                    for teacher in course.teachers.all()
                ],
                "sections": [
                    {
                        "section_number": section.section_number,
                        "capacity": section.capacity,
                        "enrolled_count": section.enrolled_students.count(),
                        "section_class": [
                            {
                                "day": section_class.get_day_display(),
                                "start_time": section_class.start_time,
                                "end_time": section_class.end_time,
                                "location": section_class.location,
                            }
                            for section_class in section.section_class.all()
                        ]
                    }
                    for section in course.course_sections.all()
                ]
            })
        days = ["อาทิตย์", "จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกย์", "เสาร์"]
        context = {"courses": data, "days": days, "times": list(range(12)), user: user}
        return render(request, "registration.html", context)
    def post(self, request):
        
        pass    