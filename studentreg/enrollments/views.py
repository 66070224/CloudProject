from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response

from courses.models import Course, Section, Class
from departments.models import Semester
from personnels.models import Student, Payment, Registra
from enrollments.models import Enroll, Grade

from django.db import transaction, IntegrityError

from enrollments.forms import GradeForm

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class IndexView(LoginRequiredMixin, View):
    def get(self, request):

        if not request.user.is_registra:
            return redirect(reverse("home"))

        return render(request, 'enrollments/index.html')



#----------------------------------------------------------------------------------------------------------------------------
# ENROLL
#----------------------------------------------------------------------------------------------------------------------------
class EnrollView(LoginRequiredMixin, View):
    def get(self, request):

        if not request.user.is_student:
            return redirect(reverse("home"))
        
        try:
            student = Student.objects.get(user=request.user)
            if student.enrolled: return redirect(reverse("home"))
            semester = Semester.objects.first()
            courses = Course.objects.filter(year=student.student_year, term=semester.term)
            return render(request, 'enrollments/enroll.html', {"courses": courses})
        except Student.DoesNotExist:
            return redirect(reverse("home"))
        except Semester.DoesNotExist:
            return Response("No semester found", status=500)
        
    
class EnrollListView(LoginRequiredMixin, View):
    def get(self, request):

        if not request.user.is_registra:
            return redirect(reverse("home"))

        registra = Registra.objects.get(user=request.user)
        enrolls = Enroll.objects.filter(section__course__department__faculty=registra.faculty, status="pen").order_by("date")
        return render(request, 'enrollments/list/enroll.html', {"enrolls": enrolls})

class EnrollConfirmListView(LoginRequiredMixin, View):
    def get(self, request):

        if not request.user.is_registra:
            return redirect(reverse("home"))

        registra = Registra.objects.get(user=request.user)
        enrolls = Enroll.objects.filter(section__course__department__faculty=registra.faculty, status="con").order_by("date")
        return render(request, 'enrollments/list/confirm.html', {"enrolls": enrolls})



#----------------------------------------------------------------------------------------------------------------------------
# GRADE
#----------------------------------------------------------------------------------------------------------------------------
class GradeView(LoginRequiredMixin, View):
    def get(self, request, id):
        enroll = Enroll.objects.get(id=id)
        grade = Grade.objects.get(enroll=enroll)
        form = GradeForm(instance=grade)
        return render(request, "enrollments/grade/student.html", {"form": form})
    def post(self, request, id):
        enroll = Enroll.objects.get(id=id)
        grade = Grade.objects.get(enroll=enroll)
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect(reverse("enrollment_enroll_list"))
        return render(request, "enrollments/grade/student.html", {"form": form})


#----------------------------------------------------------------------------------------------------------------------------
# API
#----------------------------------------------------------------------------------------------------------------------------
class SubmitAPI(LoginRequiredMixin, APIView):
    def get(self, request, courses):
        student = Student.objects.get(user=request.user)
        splitcourses = str(courses).split(",")
        try:
            with transaction.atomic():
                for course_with_sec in splitcourses:
                    if course_with_sec == "": continue
                    course_code, sec_num = course_with_sec.split("_")
                    section = Section.objects.get(course__code=course_code, number=sec_num)

                    count = Enroll.objects.filter(section=section).count()

                    if (section.capacity < count):
                        return Response({
                            "text": f"วิชา {section.course.name} เซ็ค {section.number} เต็มแล้ว"
                        }, status=400)


                    new_classes = Class.objects.filter(section=section)
                    existing_classes = Class.objects.filter(section__enrolls__student=student)
                    for new_class in new_classes:
                        for exist_class in existing_classes:
                            if new_class.day == exist_class.day:
                                if (
                                    new_class.start_time < exist_class.end_time
                                    and exist_class.start_time < new_class.end_time
                                ):
                                    return Response({
                                        "text": f"วิชา {section.course.name} ({section.number}) เวลา {new_class.day} {new_class.start_time}-{new_class.end_time} ทับกับ {exist_class.section.course.name} ({exist_class.section.number})"
                                    }, status=400)

                    enroll = Enroll(student=student, course=section.course, section=section)
                    enroll.save()
                    grade = Grade(enroll=enroll)
                    grade.save()
                    student.enrolled = True
                    student.save()
                semester = Semester.objects.first()
                payment = Payment(student=student, student_year=student.student_year, term=semester.term)
                payment.save()
            return Response({"text": "Success"}, status=200)
        except IntegrityError as e:
            return Response({"text": "คุณเคยลงวิชานี้ไปแล้ว"}, status=500)
        except Exception as e:
            print(e)
            return Response({"text": "Error"}, status=500)

class ConfirmAPI(LoginRequiredMixin, APIView):
    def get(self, request, id, text):

        if not request.user.is_registra:
            return redirect(reverse("home"))

        enroll = Enroll.objects.get(id=id)
        if text == "c":
            enroll.status = "con"
            enroll.save()
        elif text == "r":
            enroll.delete()
        return redirect(request.META['HTTP_REFERER'])
    
class RefundAPI(LoginRequiredMixin, APIView):
    def get(self, request, id):

        if not request.user.is_registra:
            return redirect(reverse("home"))

        enroll = Enroll.objects.get(id=id)
        enroll.delete()
        return redirect(request.META['HTTP_REFERER'])
    
