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
                "sections": [
                    {
                        "id": section.id,
                        "section_number": section.section_number,
                        "teacher": section.teacher.from_user.title + section.teacher.from_user.first_name + " " + section.teacher.from_user.last_name,
                        "day": section.day,
                        "start_time": section.start_time,
                        "end_time": section.end_time,
                        "location": section.location,
                        "capacity": section.capacity,
                        "enrolled_count": section.enrolled_students.count(),
                    }
                    for section in course.course_sections.all()
                ]
            })
        context = {"courses": data}
        return render(request, "registration.html", context)
    def post(self, request):
        
        pass

@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('home')