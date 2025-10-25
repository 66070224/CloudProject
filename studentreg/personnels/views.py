from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from personnels.forms import StudentForm, CustomerUserForm, ProfessorForm, RegistraForm, PayForm, EditCustomerUserForm
from django.db import transaction
from personnels.models import Student, Professor, Registra, Payment
from accounts.models import CustomUser

# Create your views here.
class CreateStudentView(View):
    def get(self, request):
        userform = CustomerUserForm()
        studentform = StudentForm()
        return render(request, "personnels/createstudent.html", {"userform": userform, "studentform": studentform})
    def post(self, request):
        userform = CustomerUserForm(request.POST, request.FILES)
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
                return render(request, "personnels/createstudent.html", {"userform": userform, "studentform": studentform})
        except Exception as e:
            print(e)
            return render(request, "personnels/createstudent.html", {"userform": userform, "studentform": studentform})

class CreateProfessorView(View):
    def get(self, request):
        userform = CustomerUserForm()
        professorform = ProfessorForm()
        return render(request, "personnels/createprofessor.html", {"userform": userform, "professorform": professorform})
    def post(self, request):
        userform = CustomerUserForm(request.POST, request.FILES)
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
                return render(request, "personnels/createprofessor.html", {"userform": userform, "professorform": professorform})
        except Exception as e:
            print(e)
            return render(request, "personnels/createprofessor.html", {"userform": userform, "professorform": professorform})
        
class CreateRegistraView(View):
    def get(self, request):
        userform = CustomerUserForm()
        registraform = RegistraForm()
        return render(request, "personnels/createregistra.html", {"userform": userform, "registraform": registraform})
    def post(self, request):
        userform = CustomerUserForm(request.POST, request.FILES)
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
                return render(request, "personnels/createregistra.html", {"userform": userform, "registraform": registraform})
        except Exception as e:
            print(e)
            return render(request, "personnels/createregistra.html", {"userform": userform, "registraform": registraform})
        
class StudentListView(View):
    def get(self, request):
        registra = Registra.objects.get(user_id=request.user.id)
        students = Student.objects.filter(department__faculty=registra.faculty)
        return render(request, "personnels/student.html", {"students": students})

class ProfessorListView(View):
    def get(self, request):
        registra = Registra.objects.get(user_id=request.user.id)
        professors = Professor.objects.filter(department__faculty=registra.faculty)
        return render(request, "personnels/professor.html", {"professors": professors})
    
class PaymentListView(View):
    def get(self, request):
        registra = Registra.objects.get(user_id=request.user.id)
        payments = Payment.objects.filter(department__faculty=registra.faculty, pay__in=("W", "N"))
        return render(request, "personnels/termfeelist.html", {"payments": payments})
    
class MyPaymentView(View):
    def get(self, request):
        student = Student.objects.get(user_id=request.user.id)
        payments = Payment.objects.filter(student=student)
        return render(request, "personnels/termfee.html", {"payments": payments})
        
class PayView(View):
    def get(self, request, id):
        student = Student.objects.get(user_id=request.user.id)
        payment = Payment.objects.get(student=student, id=id)
        form = PayForm(instance=payment)
        return render(request, "personnels/pay.html", {"form": form, "price": payment.department.term_fees})
    def post(self, request, id):
        student = Student.objects.get(user_id=request.user.id)
        payment = Payment.objects.get(student=student, id=id)
        form = PayForm(request.POST, request.FILES, instance=payment)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.pay = "W"
            payment.save()
            return redirect(reverse("mytermfee"))
        return render(request, "personnels/pay.html", {"form": form})
    
class PaymentDetailView(View):
    def get(self, request, id):
        payment = Payment.objects.get(id=id)
        return render(request, "personnels/paymentdetail.html", {"payment": payment})
    def post(self, request, id):
        payment = Payment.objects.get(id=id)
        payment.pay = "Y"
        payment.save()
        return redirect(reverse("termfeelist"))

class EditProfessorView(View):
    def get(self, request, id):
        user = CustomUser.objects.get(id=id)
        professor = Professor.objects.get(user=user)
        userform = EditCustomerUserForm(instance=user)
        professorform = ProfessorForm(instance=professor)
        return render(request, "personnels/editprofessor.html", {"userform": userform, "professorform": professorform})
    def post(self, request):
        user = CustomUser.objects.get(id=id)
        professor = Professor.objects.get(user=user)
        userform = EditCustomerUserForm(request.POST, request.FILES, instance=user)
        professorform = ProfessorForm(request.POST, instance=professor)
        try:
            with transaction.atomic():
                if userform.is_valid() and professorform.is_valid():
                    userform.save()
                    professorform.save()
                    return redirect(reverse("edit"))
                return render(request, "personnels/editprofessor.html", {"userform": userform, "professorform": professorform})
        except Exception as e:
            print(e)
            return render(request, "personnels/editprofessor.html", {"userform": userform, "professorform": professorform})