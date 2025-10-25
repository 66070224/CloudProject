from django.urls import path
from personnels.views import CreateStudentView, CreateProfessorView, CreateRegistraView, StudentListView, ProfessorListView, PaymentListView, MyPaymentView

urlpatterns = [
    path('mytermfee', MyPaymentView.as_view(), name="mytermfee"),
    path('studentlist', StudentListView.as_view(), name="studentlist"),
    path('professorlist', ProfessorListView.as_view(), name="professorlist"),
    path('termfeelist', PaymentListView.as_view(), name="termfeelist"),
    path('craetestudent', CreateStudentView.as_view(), name="createstudent"),
    path('craeteprofessor', CreateProfessorView.as_view(), name="createprofessor"),
    path('craeteregistra', CreateRegistraView.as_view(), name="createregistra"),
]