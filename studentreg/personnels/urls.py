from django.urls import path
from personnels.views import *

urlpatterns = [
    path('mytermfee', MyPaymentView.as_view(), name="mytermfee"),
    path('pay/<int:id>', PayView.as_view(), name="pay"),
    path('studentlist', StudentListView.as_view(), name="studentlist"),
    path('editstudent/<int:id>', EditStudentView.as_view(), name="editstudent"),
    path('professorlist', ProfessorListView.as_view(), name="professorlist"),
    path('editprofessor/<int:id>', EditProfessorView.as_view(), name="editprofessor"),
    path('termfeelist', PaymentListView.as_view(), name="termfeelist"),
    path('paymentdetail/<int:id>', PaymentDetailView.as_view(), name="paymentdetail"),
    path('craetestudent', CreateStudentView.as_view(), name="createstudent"),
    path('craeteprofessor', CreateProfessorView.as_view(), name="createprofessor"),
    path('craeteregistra', CreateRegistraView.as_view(), name="createregistra"),
]