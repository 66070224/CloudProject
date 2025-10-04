from django.shortcuts import render, redirect
from django.views import View
from . import forms, models
from django.db import transaction

class StaffHomeView(View):
    def get(self, request):

        return render(request, "home.html", context={

        })
    
class ManageStudentView(View):
    def get(self, request):
        invalid = request.session.pop("invalid", False)
        students = models.Student.objects.all()
        form = forms.StudentForm(invalid) if invalid else forms.StudentForm()

        return render(request, "manage_student.html", context={
            "students": students, "is_invalid": invalid, "form": form
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
        student = models.Student.objects.get(code=student_code)
        form = forms.StudentForm(invalid, instance=student) if invalid else forms.StudentForm(instance=student)

        return render(request, "edit_student.html", context={
            "form": form,
        })
    def post(self, request, student_code):
        student = models.Student.objects.get(code=student_code)
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