from django.urls import path
from personnels.views import *

urlpatterns = [
    path('termfee', MyPaymentView.as_view(), name="personel_termfee_list"),
    path('termfee/pay/<int:id>', PayView.as_view(), name="personel_termfee_pay"),

    path('student', StudentListView.as_view(), name="personel_student_list"),
    path('student/create', CreateStudentView.as_view(), name="personel_student_create"),
    path('student/edit/<int:id>', EditStudentView.as_view(), name="personel_student_edit"),

    path('professor', ProfessorListView.as_view(), name="personel_professor_list"),
    path('professor/create', CreateProfessorView.as_view(), name="personel_professor_create"),
    path('professor/edit/<int:id>', EditProfessorView.as_view(), name="personel_professor_edit"),
    
    path('registra', RegistralistView.as_view(), name="personel_registra_list"),
    path('registra/create', CreateRegistraView.as_view(), name="personel_registra_create"),
    path('registra/edit/<int:id>', EditRegistraView.as_view(), name="personel_registra_edit"),

    path('payment', PaymentListView.as_view(), name="personel_payment_list"),
    path('payment/<int:id>', PaymentDetailView.as_view(), name="personel_payment_detail"),

    path('api/delete/registra/<int:id>', DeleteRegistraAPI.as_view(), name="personel_api_delete_registra"),
    path('api/delete/professor/<int:id>', DeleteProfessorAPI.as_view(), name="personel_api_delete_professor"),
    path('api/delete/student/<int:id>', DeleteStudentAPI.as_view(), name="personel_api_delete_student"),
   
]