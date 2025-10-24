from django.urls import path
from personnels.views import CreateStudentView, CreateProfessorView, CreateRegistraView

urlpatterns = [
    path('craetestudent', CreateStudentView.as_view(), name="createstudent"),
    path('craeteprofessor', CreateProfessorView.as_view(), name="createprofessor"),
    path('craeteregistra', CreateRegistraView.as_view(), name="createregistra"),
]