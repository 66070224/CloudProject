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
        return render(request, "personnels/create/student.html", {"userform": userform, "studentform": studentform})
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
                return render(request, "personnels/create/student.html", {"userform": userform, "studentform": studentform})
        except Exception as e:
            print(e)
            return render(request, "personnels/create/student.html", {"userform": userform, "studentform": studentform})

class CreateProfessorView(View):
    def get(self, request):
        userform = CustomerUserForm()
        professorform = ProfessorForm()
        return render(request, "personnels/create/professor.html", {"userform": userform, "professorform": professorform})
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
                return render(request, "personnels/create/professor.html", {"userform": userform, "professorform": professorform})
        except Exception as e:
            print(e)
            return render(request, "personnels/create/professor.html", {"userform": userform, "professorform": professorform})
        
class CreateRegistraView(View):
    def get(self, request):
        userform = CustomerUserForm()
        registraform = RegistraForm()
        return render(request, "personnels/create/registra.html", {"userform": userform, "registraform": registraform})
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
                return render(request, "personnels/create/registra.html", {"userform": userform, "registraform": registraform})
        except Exception as e:
            print(e)
            return render(request, "personnels/create/registra.html", {"userform": userform, "registraform": registraform})
        
class StudentListView(View):
    def get(self, request):

        text = request.GET.get("text")
        type = request.GET.get("type")

        registra = Registra.objects.get(user_id=request.user.id)
        students = Student.objects.filter(department__faculty=registra.faculty)

        if text and type and text != "None":
            if type == "id":
                students = students.filter(student_id__icontains=text)
            elif type == "name":
                students = students.filter(user__first_name__icontains=text)
            elif type == "year":
                students = students.filter(year=text)
            elif type == "department":
                students = students.filter(department__name__icontains=text)
            elif type == "faculty":
                students = students.filter(department__faculty__name__icontains=text)
        
        if text == "None" or text == None:
            text = ""

        return render(request, "personnels/list/student.html", {"students": students, "text": text, "type": type})

class ProfessorListView(View):
    def get(self, request):
        text = request.GET.get("text")
        type = request.GET.get("type")

        registra = Registra.objects.get(user_id=request.user.id)
        professors = Professor.objects.filter(department__faculty=registra.faculty)

        if text and type and text != "None":
            if type == "name":
                professors = professors.filter(user__first_name__icontains=text)
            elif type == "department":
                professors = professors.filter(department__name__icontains=text)
            elif type == "faculty":
                professors = professors.filter(department__faculty__name__icontains=text)

        if text == "None" or text == None:
            text = ""

        return render(request, "personnels/list/professor.html", {"professors": professors, "text": text, "type": type})
    
class PaymentListView(View):
    def get(self, request):
        registra = Registra.objects.get(user_id=request.user.id)
        payments = Payment.objects.filter(department__faculty=registra.faculty, pay__in=("W", "N"))
        return render(request, "personnels/list/termfee.html", {"payments": payments})
    
class MyPaymentView(View):
    def get(self, request):
        student = Student.objects.get(user_id=request.user.id)
        payments = Payment.objects.filter(student=student)
        return render(request, "personnels/student/termfee.html", {"payments": payments})
        
class PayView(View):
    def get(self, request, id):
        student = Student.objects.get(user_id=request.user.id)
        payment = Payment.objects.get(student=student, id=id)
        form = PayForm(instance=payment)
        return render(request, "personnels/student/pay.html", {"form": form, "price": payment.department.term_fees})
    def post(self, request, id):
        student = Student.objects.get(user_id=request.user.id)
        payment = Payment.objects.get(student=student, id=id)
        form = PayForm(request.POST, request.FILES, instance=payment)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.pay = "W"
            payment.save()
            return redirect(reverse("mytermfee"))
        return render(request, "personnels/student/pay.html", {"form": form})
    
class PaymentDetailView(View):
    def get(self, request, id):
        payment = Payment.objects.get(id=id)
        return render(request, "personnels/detail/payment.html", {"payment": payment})
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
        return render(request, "personnels/edit/professor.html", {"userform": userform, "professorform": professorform})
    def post(self, request, id):
        user = CustomUser.objects.get(id=id)
        professor = Professor.objects.get(user=user)
        userform = EditCustomerUserForm(request.POST, request.FILES, instance=user)
        professorform = ProfessorForm(request.POST, instance=professor)
        try:
            with transaction.atomic():
                if userform.is_valid() and professorform.is_valid():
                    userform.save()
                    professorform.save()
                    return redirect(reverse("professorlist"))
                return render(request, "personnels/edit/professor.html", {"userform": userform, "professorform": professorform})
        except Exception as e:
            print(e)
            return render(request, "personnels/edit/professor.html", {"userform": userform, "professorform": professorform})
        
class EditStudentView(View):
    def get(self, request, id):
        user = CustomUser.objects.get(id=id)
        student = Student.objects.get(user=user)
        userform = EditCustomerUserForm(instance=user)
        studentform = StudentForm(instance=student)
        return render(request, "personnels/edit/student.html", {"userform": userform, "studentform": studentform})
    def post(self, request, id):
        user = CustomUser.objects.get(id=id)
        student = Student.objects.get(user=user)
        userform = EditCustomerUserForm(request.POST, request.FILES, instance=user)
        studentform = StudentForm(request.POST, instance=student)
        try:
            with transaction.atomic():
                if userform.is_valid() and studentform.is_valid():
                    userform.save()
                    studentform.save()
                    return redirect(reverse("studentlist"))
                return render(request, "personnels/edit/student.html", {"userform": userform, "studentform": studentform})
        except Exception as e:
            print(e)
            return render(request, "personnels/edit/student.html", {"userform": userform, "studentform": studentform})