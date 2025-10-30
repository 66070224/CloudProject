from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from personnels.forms import StudentForm, CustomerUserForm, ProfessorForm, RegistraForm, PayForm, EditCustomerUserForm
from django.db import transaction, Error
from personnels.models import Student, Professor, Registra, Payment
from accounts.models import CustomUser
from departments.models import Faculty, Department

from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.services import CognitoService

cognito = CognitoService()

from rest_framework.views import APIView

from django.db.models import F, Q, Value, CharField
from django.db.models.functions import Concat

#----------------------------------------------------------------------------------------------------------------------------
# STUDENT
#----------------------------------------------------------------------------------------------------------------------------
class StudentListView(LoginRequiredMixin, View):
    def get(self, request):

        if not request.user.is_registra:
            return redirect(reverse("home"))

        student_id = request.GET.get("student_id")
        name = request.GET.get("name")
        year = request.GET.get("year")
        department = request.GET.get("department_select")

        registra = Registra.objects.get(user_id=request.user.id)
        students = Student.objects.filter(department__faculty=registra.faculty).annotate(fully_name=Concat(F("user__title"), Value(" "), F("user__first_name"), Value(" "), F("user__last_name"), output_field=CharField()))
        departments = Department.objects.filter(faculty=registra.faculty)

        if student_id and student_id != "None":
            students = students.filter(student_id__icontains=student_id)
        if name and name != "None":
            students = students.filter(fully_name__icontains=name)
        if year and year != "None":
            students = students.filter(student_year=year)
        if department and department != "None":
            students = students.filter(department__name__icontains=department)

        if student_id == "None" or student_id == None:
            student_id = ""
        if name == "None" or name == None:
            name = ""
        if year == "None" or year == None:
            year = ""
        if department == "None" or department == None:
            department = ""

        return render(request, "personnels/list/student.html", {"students": students, "name": name, "student_id": student_id, "year": year, "department_select": department, "departments": departments})
    
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
                    email = userform.cleaned_data.get('email')
                    password = userform.cleaned_data.get('password1')
                    user = userform.save(commit=False)
                    user.role = "stu"
                    student = studentform.save(commit=False)
                    student.user = user
                    user.save()
                    student.save()
                    created_result = cognito.create_user_cognito(email=email, password=password)
                    if created_result["status"]:
                        return redirect(reverse("personel_student_list"))
                    else:
                        raise Error('สร้าง User ใน Cognito ไม่สำเร็จ')
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
        email = user.email
        student = Student.objects.get(user=user)
        userform = EditCustomerUserForm(request.POST, request.FILES, instance=user)
        studentform = StudentForm(request.POST, instance=student)
        try:
            with transaction.atomic():
                if userform.is_valid() and studentform.is_valid():
                    new_email = userform.cleaned_data.get('email')
                    userform.save()
                    studentform.save()
                    success = cognito.update_user_email_cognito(email=email, new_email=new_email)
                    if success:
                        print("Update email success")
                    else:
                        raise Error('Update email failed')
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

        name = request.GET.get("name")

        registra = Registra.objects.get(user=request.user)
        professors = Professor.objects.filter(faculty=registra.faculty).annotate(fully_name=Concat(F("user__title"), Value(" "), F("user__first_name"), Value(" "), F("user__last_name"), output_field=CharField()))

        if name and name != "None":
            professors = professors.filter(fully_name__icontains=name)

        if name == "None" or name == None:
            name = ""

        return render(request, "personnels/list/professor.html", {"professors": professors, "name": name })
    
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
                    email = userform.cleaned_data.get('email')
                    password = userform.cleaned_data.get('password1')
                    user = userform.save(commit=False)
                    user.role = "pro"
                    professor = professorform.save(commit=False)
                    professor.user = user
                    user.save()
                    professor.save()
                    created_result = cognito.create_user_cognito(email=email, password=password)
                    if created_result["status"]:
                        return redirect(reverse("personel_professor_list"))
                    else:
                        raise Error('สร้าง User ใน Cognito ไม่สำเร็จ')
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
        email = user.email
        professor = Professor.objects.get(user=user)
        userform = EditCustomerUserForm(request.POST, request.FILES, instance=user)
        professorform = ProfessorForm(request.POST, instance=professor)
        try:
            with transaction.atomic():
                if userform.is_valid() and professorform.is_valid():
                    new_email = userform.cleaned_data.get('email')
                    userform.save()
                    professorform.save()
                    success = cognito.update_user_email_cognito(email=email, new_email=new_email)
                    if success:
                        print("Update email success")
                    else:
                        raise Error('Update email failed')
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

        name = request.GET.get("name")
        faculty = request.GET.get("faculty")

        registras = Registra.objects.all().annotate(fully_name=Concat(F("user__title"), Value(" "), F("user__first_name"), Value(" "), F("user__last_name"), output_field=CharField()))

        if name and name != "None":
            registras = registras.filter(fully_name__icontains=name)
        if faculty and faculty != "None":
            registras = registras.filter(faculty__name__icontains=faculty)

        if name == "None" or name == None:
            name = ""
        if faculty == "None" or faculty == None:
            faculty = ""

        return render(request, "personnels/list/registra.html", {"registras": registras, "name": name, "faculty": faculty, "faculties": Faculty.objects.all()})
        
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
                    email = userform.cleaned_data.get('email')
                    password = userform.cleaned_data.get('password1')
                    user = userform.save(commit=False)
                    user.role = "reg"
                    registra = registraform.save(commit=False)
                    registra.user = user
                    user.save()
                    registra.save()
                    created_result = cognito.create_user_cognito(email=email, password=password)
                    if created_result["status"]:
                        return redirect(reverse("personel_registra_list"))
                    else:
                        raise Error('สร้าง User ใน Cognito ไม่สำเร็จ')
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
        email = user.email
        registra = Registra.objects.get(user=user)
        userform = EditCustomerUserForm(request.POST, request.FILES, instance=user)
        registraform = RegistraForm(request.POST, instance=registra)
        try:
            with transaction.atomic():
                if userform.is_valid() and registraform.is_valid():
                    new_email = userform.cleaned_data.get('email')
                    userform.save()
                    registraform.save()

                    success = cognito.update_user_email_cognito(email=email, new_email=new_email)
                    if success:
                        print("Update email success")
                    else:
                        raise Error('Update email failed')
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
                success = cognito.delete_user_cognito(user.email)
                if success:
                    print("User deleted successfully")
                else:
                    raise Error('ไม่สามารถลบ User ออกจาก Cognito ได้')
                return redirect(request.META['HTTP_REFERER'])
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
                success = cognito.delete_user_cognito(user.email)
                if success:
                    print("User deleted successfully")
                else:
                    raise Error('ไม่สามารถลบ User ออกจาก Cognito ได้')
                return redirect(request.META['HTTP_REFERER'])
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
                success = cognito.delete_user_cognito(user.email)
                if success:
                    print("User deleted successfully")
                else:
                    raise Error('ไม่สามารถลบ User ออกจาก Cognito ได้')
                return redirect(request.META['HTTP_REFERER'])
        except user.DoesNotExist:
            return redirect(reverse("home"))
        except Student.DoesNotExist:
            return redirect(reverse("home"))
        
