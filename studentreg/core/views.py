from django.shortcuts import render
from django.views import View

from enrollments.models import Enroll
from personnels.models import Student

import json

# Create your views here.
class HomeView(View):
    def get(self, request):
        context = {}
        if request.user.role == "stu":
            student = Student.objects.get(user_id=request.user.id)
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
        return render(request, 'home.html', context)