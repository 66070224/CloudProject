from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from personnels.forms import StudentForm, CustomerUserForm, ProfessorForm, RegistraForm
from django.db import transaction

# Create your views here.
class CreateStudentView(View):
    def get(self, request):
        userform = CustomerUserForm()
        studentform = StudentForm()
        return render(request, "createstudent.html", {"userform": userform, "studentform": studentform})
    def post(self, request):
        userform = CustomerUserForm(data=request.POST)
        studentform = StudentForm(data=request.POST)
        try:
            with transaction.atomic():
                if userform.is_valid() and studentform.is_valid():
                    user = userform.save(commit=False)
                    user.role = "stu"
                    student = studentform.save(commit=False)
                    student.user = user
                    user.save()
                    student.save()
                    return redirect(reverse("createstudent"))
                return render(request, "createstudent.html", {"userform": userform, "studentform": studentform})
        except Exception as e:
            print(e)
            return render(request, "createstudent.html", {"userform": userform, "studentform": studentform})

class CreateProfessorView(View):
    def get(self, request):
        userform = CustomerUserForm()
        professorform = ProfessorForm()
        return render(request, "createstudent.html", {"userform": userform, "studentform": professorform})
    def post(self, request):
        userform = CustomerUserForm(data=request.POST)
        professorform = ProfessorForm(data=request.POST)
        try:
            with transaction.atomic():
                if userform.is_valid() and professorform.is_valid():
                    user = userform.save(commit=False)
                    user.role = "pro"
                    professor = professorform.save(commit=False)
                    professor.user = user
                    user.save()
                    professor.save()
                    return redirect(reverse("createprofessor"))
                return render(request, "createstudent.html", {"userform": userform, "studentform": professorform})
        except Exception as e:
            print(e)
            return render(request, "createstudent.html", {"userform": userform, "studentform": professorform})
        
class CreateRegistraView(View):
    def get(self, request):
        userform = CustomerUserForm()
        registraform = RegistraForm()
        return render(request, "createstudent.html", {"userform": userform, "studentform": registraform})
    def post(self, request):
        userform = CustomerUserForm(data=request.POST)
        registraform = RegistraForm(data=request.POST)
        try:
            with transaction.atomic():
                if userform.is_valid() and registraform.is_valid():
                    user = userform.save(commit=False)
                    user.role = "reg"
                    registra = registraform.save(commit=False)
                    registra.user = user
                    user.save()
                    registra.save()
                    return redirect(reverse("createregistra"))
                return render(request, "createstudent.html", {"userform": userform, "studentform": registraform})
        except Exception as e:
            print(e)
            return render(request, "createstudent.html", {"userform": userform, "studentform": registraform})


