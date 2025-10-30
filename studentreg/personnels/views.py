from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from personnels.forms import StudentForm, CustomerUserForm, ProfessorForm, RegistraForm, PayForm, EditCustomerUserForm
from django.db import transaction
from personnels.models import Student, Professor, Registra, Payment
from accounts.models import CustomUser

from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.views import APIView

#----------------------------------------------------------------------------------------------------------------------------
# STUDENT
#----------------------------------------------------------------------------------------------------------------------------
class StudentListView(LoginRequiredMixin, View):
    def get(self, request):

        if not request.user.is_registra:
            return redirect(reverse("home"))

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
    
class CreateStudentView(LoginRequiredMixin, View):
    def get(self, request):
        
        if not request.user.is_registra:
            return redirect(reverse("home"))

        userform = CustomerUserForm()
        studentform = StudentForm()
        return render(request, "personnels/create/student.html", {"userform": userform, "studentform": studentform})
    def post(self, request):
        
        if not request.user.is_registra:
            return redirect(reverse("home"))

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
                    return redirect(reverse("personel_student_list"))
                return render(request, "personnels/create/student.html", {"userform": userform, "studentform": studentform})
        except Exception as e:
            print(e)
            return render(request, "personnels/create/student.html", {"userform": userform, "studentform": studentform})
        
class EditStudentView(LoginRequiredMixin, View):
    def get(self, request, id):
        
        if not request.user.is_registra:
            return redirect(reverse("home"))

        user = CustomUser.objects.get(id=id)
        student = Student.objects.get(user=user)
        userform = EditCustomerUserForm(instance=user)
        studentform = StudentForm(instance=student)
        return render(request, "personnels/edit/student.html", {"userform": userform, "studentform": studentform})
    def post(self, request, id):
        
        if not request.user.is_registra:
            return redirect(reverse("home"))

        user = CustomUser.objects.get(id=id)
        student = Student.objects.get(user=user)
        userform = EditCustomerUserForm(request.POST, request.FILES, instance=user)
        studentform = StudentForm(request.POST, instance=student)
        try:
            with transaction.atomic():
                if userform.is_valid() and studentform.is_valid():
                    userform.save()
                    studentform.save()
                    return redirect(reverse("personel_student_list"))
                return render(request, "personnels/edit/student.html", {"userform": userform, "studentform": studentform})
        except Exception as e:
            print(e)
            return render(request, "personnels/edit/student.html", {"userform": userform, "studentform": studentform})



#----------------------------------------------------------------------------------------------------------------------------
# PROFESSOR
#----------------------------------------------------------------------------------------------------------------------------
class ProfessorListView(LoginRequiredMixin, View):
    def get(self, request):
        
        if not request.user.is_registra:
            return redirect(reverse("home"))

        text = request.GET.get("text")
        type = request.GET.get("type")

        registra = Registra.objects.get(user_id=request.user.id)
        professors = Professor.objects.filter(faculty=registra.faculty)

        if text and type and text != "None":
            if type == "name":
                professors = professors.filter(user__first_name__icontains=text)

        if text == "None" or text == None:
            text = ""

        return render(request, "personnels/list/professor.html", {"professors": professors, "text": text, "type": type})
    
class CreateProfessorView(LoginRequiredMixin, View):
    def get(self, request):
        
        if not request.user.is_registra:
            return redirect(reverse("home"))

        userform = CustomerUserForm()
        professorform = ProfessorForm()
        return render(request, "personnels/create/professor.html", {"userform": userform, "professorform": professorform})
    def post(self, request):
        
        if not request.user.is_registra:
            return redirect(reverse("home"))

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
                    return redirect(reverse("personel_professor_list"))
                return render(request, "personnels/create/professor.html", {"userform": userform, "professorform": professorform})
        except Exception as e:
            print(e)
            return render(request, "personnels/create/professor.html", {"userform": userform, "professorform": professorform})
        
class EditProfessorView(LoginRequiredMixin, View):
    def get(self, request, id):
        
        if not request.user.is_registra:
            return redirect(reverse("home"))

        user = CustomUser.objects.get(id=id)
        professor = Professor.objects.get(user=user)
        userform = EditCustomerUserForm(instance=user)
        professorform = ProfessorForm(instance=professor)
        return render(request, "personnels/edit/professor.html", {"userform": userform, "professorform": professorform})
    def post(self, request, id):
        
        if not request.user.is_registra:
            return redirect(reverse("home"))

        user = CustomUser.objects.get(id=id)
        professor = Professor.objects.get(user=user)
        userform = EditCustomerUserForm(request.POST, request.FILES, instance=user)
        professorform = ProfessorForm(request.POST, instance=professor)
        try:
            with transaction.atomic():
                if userform.is_valid() and professorform.is_valid():
                    userform.save()
                    professorform.save()
                    return redirect(reverse("personel_professor_list"))
                return render(request, "personnels/edit/professor.html", {"userform": userform, "professorform": professorform})
        except Exception as e:
            print(e)
            return render(request, "personnels/edit/professor.html", {"userform": userform, "professorform": professorform})



#----------------------------------------------------------------------------------------------------------------------------
# REGISTRA
#----------------------------------------------------------------------------------------------------------------------------
class RegistralistView(LoginRequiredMixin, View):
    def get(self, request):

        if not request.user.is_admin:
            return redirect(reverse("home"))

        text = request.GET.get("text")
        type = request.GET.get("type")

        registras = Registra.objects.all()

        if text and type and text != "None":
            if type == "name":
                registras = registras.filter(user__first_name__icontains=text)
            elif type == "faculty":
                registras = registras.filter(faculty__name__icontains=text)

        if text == "None" or text == None:
            text = ""

        return render(request, "personnels/list/registra.html", {"registras": registras, "text": text, "type": type})
        
class CreateRegistraView(LoginRequiredMixin, View):
    def get(self, request):

        if not request.user.is_admin:
            return redirect(reverse("home"))

        userform = CustomerUserForm()
        registraform = RegistraForm()
        return render(request, "personnels/create/registra.html", {"userform": userform, "registraform": registraform})
    def post(self, request):

        if not request.user.is_admin:
            return redirect(reverse("home"))

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
                    return redirect(reverse("personel_registra_list"))
                return render(request, "personnels/create/registra.html", {"userform": userform, "registraform": registraform})
        except Exception as e:
            print(e)
            return render(request, "personnels/create/registra.html", {"userform": userform, "registraform": registraform})
        
class EditRegistraView(LoginRequiredMixin, View):
    def get(self, request, id):

        if not request.user.is_admin:
            return redirect(reverse("home"))

        user = CustomUser.objects.get(id=id)
        registra = Registra.objects.get(user=user)
        userform = EditCustomerUserForm(instance=user)
        registraform = RegistraForm(instance=registra)
        return render(request, "personnels/edit/registra.html", {"userform": userform, "registraform": registraform})
    def post(self, request, id):

        if not request.user.is_admin:
            return redirect(reverse("home"))

        user = CustomUser.objects.get(id=id)
        registra = Registra.objects.get(user=user)
        userform = EditCustomerUserForm(request.POST, request.FILES, instance=user)
        registraform = RegistraForm(request.POST, instance=registra)
        try:
            with transaction.atomic():
                if userform.is_valid() and registraform.is_valid():
                    userform.save()
                    registraform.save()
                    return redirect(reverse("personel_registra_list"))
                return render(request, "personnels/edit/registra.html", {"userform": userform, "registraform": registraform})
        except Exception as e:
            print(e)
            return render(request, "personnels/edit/registra.html", {"userform": userform, "registraform": registraform})



#----------------------------------------------------------------------------------------------------------------------------
# PAYMENT
#----------------------------------------------------------------------------------------------------------------------------
class PaymentListView(LoginRequiredMixin, View):
    def get(self, request):
        
        if not request.user.is_registra:
            return redirect(reverse("home"))

        registra = Registra.objects.get(user=request.user)
        payments = Payment.objects.filter(student__department__faculty=registra.faculty, status__in=("W", "N"))
        return render(request, "personnels/list/termfee.html", {"payments": payments})
    
class MyPaymentView(LoginRequiredMixin, View):
    def get(self, request):
        
        if not request.user.is_student:
            return redirect(reverse("home"))

        student = Student.objects.get(user=request.user)
        payments = Payment.objects.filter(student=student)
        return render(request, "personnels/student/termfee.html", {"payments": payments})
        
class PayView(LoginRequiredMixin, View):
    def get(self, request, id):
        
        if not request.user.is_student:
            return redirect(reverse("home"))

        student = Student.objects.get(user=request.user)
        payment = Payment.objects.get(student=student, id=id)
        form = PayForm(instance=payment)
        return render(request, "personnels/student/pay.html", {"form": form, "price": payment.student.department.term_fees})
    def post(self, request, id):
        
        if not request.user.is_student:
            return redirect(reverse("home"))

        student = Student.objects.get(user_id=request.user.id)
        payment = Payment.objects.get(student=student, id=id)
        form = PayForm(request.POST, request.FILES, instance=payment)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.status = "W"
            payment.save()
            return redirect(reverse("personel_termfee_list"))
        return render(request, "personnels/student/pay.html", {"form": form})
    
class PaymentDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        
        if not request.user.is_registra:
            return redirect(reverse("home"))

        payment = Payment.objects.get(id=id)
        return render(request, "personnels/detail/payment.html", {"payment": payment})
    def post(self, request, id):
        
        if not request.user.is_registra:
            return redirect(reverse("home"))

        payment = Payment.objects.get(id=id)
        payment.status = "Y"
        payment.save()
        return redirect(reverse("personel_payment_list"))


#----------------------------------------------------------------------------------------------------------------------------
# API
#----------------------------------------------------------------------------------------------------------------------------

class DeleteRegistraAPI(LoginRequiredMixin, APIView):
    def get(self, request, id):
        
        if not request.user.is_admin:
            return redirect(reverse("home"))

        try:
            with transaction.atomic():
                user = CustomUser.objects.get(id=id)
                registra = Registra.objects.get(user=user)
                registra.delete()
                user.delete()
                return redirect(reverse("personel_registra_list"))
        except user.DoesNotExist:
            return redirect(reverse("home"))
        except Registra.DoesNotExist:
            return redirect(reverse("home"))
        
class DeleteProfessorAPI(LoginRequiredMixin, APIView):
    def get(self, request, id):
        
        if not request.user.is_registra:
            return redirect(reverse("home"))

        try:
            with transaction.atomic():
                user = CustomUser.objects.get(id=id)
                professor = Professor.objects.get(user=user)
                professor.delete()
                user.delete()
                return redirect(reverse("personel_professor_list"))
        except user.DoesNotExist:
            return redirect(reverse("home"))
        except Professor.DoesNotExist:
            return redirect(reverse("home"))
        
class DeleteStudentAPI(LoginRequiredMixin, APIView):
    def get(self, request, id):
        
        if not request.user.is_registra:
            return redirect(reverse("home"))

        try:
            with transaction.atomic():
                user = CustomUser.objects.get(id=id)
                student = Student.objects.get(user=user)
                student.delete()
                user.delete()
                return redirect(reverse("personel_student_list"))
        except user.DoesNotExist:
            return redirect(reverse("home"))
        except Student.DoesNotExist:
            return redirect(reverse("home"))
        
