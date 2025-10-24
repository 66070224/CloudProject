from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response

from courses.models import Course, Section
from departments.models import Semester
from personnels.models import Student
from enrollments.models import Enroll

from django.db import transaction, IntegrityError

# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'enrollments/index.html')

class EnrollView(View):
    def get(self, request):
        student = Student.objects.get(user_id=request.user.id)
        semester = Semester.objects.first()
        courses = Course.objects.filter(year=student.year, term=semester.term)
        return render(request, 'enrollments/enroll.html', {"courses": courses})

class SubmitView(APIView):
    def get(self, request, courses):
        student = Student.objects.get(user_id=request.user.id)
        splitcourses = str(courses).split(",")
        try:
            with transaction.atomic():
                for course_with_sec in splitcourses:
                    if course_with_sec == "": continue
                    course_code, sec_num = course_with_sec.split("_")
                    section = Section.objects.get(course__code=course_code, number=sec_num)
                    enroll = Enroll(student=student, section=section)
                    enroll.save()
            return Response({"text": "Success"}, status=200)
        except IntegrityError as e:
            return Response({"text": "คุณเคยลงวิชานี้ไปแล้ว"}, status=500)
        except Exception as e:
            return Response({"text": "Error"}, status=500)
    
