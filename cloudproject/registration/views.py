from django.views import View
from django.shortcuts import render, redirect
from .models import Course, CourseSection
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef
from django.db.models import F


class HomeView(View):
    def get(self, request):
        user = request.user
        context = {user: user}
        return render(request, "home.html", context)

class RegistrationView(LoginRequiredMixin, View):
    login_url = 'home'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        courses = Course.objects.filter(department=request.user.userinfo.student.department).prefetch_related('course_sections')
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
                                "day": section_class.day,
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
        context = {"courses": data, "days": days, "times": list(range(12))}
        return render(request, "registration.html", context)
    def post(self, request):
        
        pass

@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('home')