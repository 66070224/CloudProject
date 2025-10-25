from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response

from courses.models import Course, Section
from departments.models import Semester
from personnels.models import Student, Payment, Registra
from enrollments.models import Enroll

from django.db import transaction, IntegrityError

# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'enrollments/index.html')

class EnrollView(View):
    def get(self, request):
        student = Student.objects.get(user_id=request.user.id)
        if student.enrolled: return redirect(reverse("home"))
        semester = Semester.objects.first()
        courses = Course.objects.filter(year=student.year, term=semester.term)
        return render(request, 'enrollments/enroll.html', {"courses": courses})

class SubmitAPI(APIView):
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
                    semester = Semester.objects.first()
                    payment = Payment(student=student, department=student.department, year=semester.year, term=semester.term)
                    payment.save()
                    student.enrolled = True
                    student.save()
            return Response({"text": "Success"}, status=200)
        except IntegrityError as e:
            return Response({"text": "คุณเคยลงวิชานี้ไปแล้ว"}, status=500)
        except Exception as e:
            return Response({"text": "Error"}, status=500)

class EnrollListView(View):
    def get(self, request):
        registra = Registra.objects.get(user_id=request.user.id)
        enrolls = Enroll.objects.filter(section__course__department__faculty=registra.faculty, status="pen").order_by("date")
        return render(request, 'enrollments/enrolllist.html', {"enrolls": enrolls})

class ConfirmAPI(APIView):
    def get(self, request, id, text):
        enroll = Enroll.objects.get(id=id)
        if text == "c":
            enroll.status = "con"
            enroll.save()
        elif text == "r":
            enroll.delete()
        return redirect(reverse("enroll_enrolllist"))