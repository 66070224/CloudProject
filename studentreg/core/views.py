from django.shortcuts import render, get_object_or_404
from django.views import View

from enrollments.models import Enroll
from personnels.models import Student, Registra, Professor

from courses.models import Course

from django.contrib.auth.mixins import LoginRequiredMixin

import json

# Create your views here.
class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        if request.user.is_student:
            student = Student.objects.get(user=request.user)
            enrolls = Enroll.objects.filter(student=student, status="con").select_related("section__course").prefetch_related("section__classes")
            enroll_data = []
            for e in enrolls:
                course = e.section.course
                classes = []
                for cls in e.section.classes.all():
                    classes.append({
                        "day": cls.day,
                        "type": cls.type,
                        "start_time": cls.start_time.strftime("%H:%M"),
                        "end_time": cls.end_time.strftime("%H:%M"),
                        "location": cls.location,
                    })

                enroll_data.append({
                    "course_code": course.code,
                    "course_name": course.name,
                    "section": e.section.number,
                    "classes": classes,
                })

            # แปลงเป็น JSON string
            context["enrolls_json"] = json.dumps(enroll_data)
        if request.user.is_registra:
            registra = Registra.objects.get(user=request.user)
            context["total_students"] = Student.objects.filter(department__faculty=registra.faculty).count()
            context["total_courses"] = Course.objects.filter(department__faculty=registra.faculty).count()
            context["total_professors"] = Professor.objects.filter(faculty=registra.faculty).count()

        if request.user.is_professor:
            professor = Professor.objects.get(user=request.user)
            context["total_courses"] = Course.objects.filter(department__faculty=professor.faculty).count()
            context["total_students"] = Student.objects.filter(department__faculty=professor.faculty).count()
        return render(request, 'home.html', context)