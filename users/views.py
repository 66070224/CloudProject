from django.shortcuts import render, redirect
from django.views import View
from . import forms
from .models import *
from academics.models import *
from enrollment.models import *
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.models import User

class StaffHomeView(View):
    def get(self, request):
        total_students = Student.objects.count()
        total_courses = Course.objects.count()
        return render(request, "home.html", context={ 'total_students': total_students, 'total_courses': total_courses })

class ManageStudentView(View):
    def get(self, request):
        # filter
        filter = request.GET.get("filter", "")
        search = request.GET.get("search", "")

        invalid = request.session.pop("invalid", False)
        form = forms.StudentForm(invalid) if invalid else forms.StudentForm()
        students = Student.objects.all()

        if search:
            if filter == "":
                students = students.filter(
                    Q(first_name__icontains=search) | Q(last_name__icontains=search)
                )
            elif filter == "email":
                students = students.filter(email__icontains=search)
            elif filter == "department":
                students = students.filter(
                    Q(department__name__icontains=search) | Q(department__faculty__name__icontains=search)
                )

        return render(request, "manage_student.html", context={
            "students": students, 
            "is_invalid": invalid, 
            "form": form,
            "filter": filter,
            "search": search,
        })
    def post(self, request):
        form = forms.StudentForm(request.POST)

        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()

                    return redirect('manage_student_view')
                
                raise transaction.TransactionManagementError("Error")
        except Exception as e:
            print(f"Error {e}")
            request.session["invalid"] = request.POST

            return redirect('manage_student_view')
    
class EditStudentView(View):
    def get(self, request, student_code):
        invalid = request.session.pop("invalid", False)
        student = Student.objects.get(code=student_code)
        form = forms.StudentForm(invalid, instance=student) if invalid else forms.StudentForm(instance=student)
        
        enrollments = EnrollStudent.objects.filter(student=student).select_related('course_section__course')
        
        return render(request, "edit_student.html", context={
            "form": form,
            'enrollments': enrollments,
        })
    def post(self, request, student_code):
        student = Student.objects.get(code=student_code)
        form = forms.StudentForm(request.POST, instance=student)

        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()

                    return redirect('manage_student_view')
                
                print(f"Invalid form: {form.errors}")
                raise transaction.TransactionManagementError("Error")
        except Exception as e:
            print(f"Error {e}")
            request.session["invalid"] = request.POST

            return redirect('edit_student_view', student_code=student_code)

class StudentProfileView(View):
    def get(self, request):
        student_code = request.session.get("student_code")
        print(f"In Student View : {student_code}")
        student = Student.objects.get(code=student_code)

        return render(request, "profile_student.html", context={
            "student": student
        })