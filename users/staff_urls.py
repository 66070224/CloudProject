from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.StaffHomeView.as_view(), name="staff_home_view"),
    path("manage_student/", views.ManageStudentView.as_view(), name="manage_student_view"),
    path("edit_student/<student_code>", views.EditStudentView.as_view(), name="edit_student_view"),
    
    path("academics/", include('academics.urls')),
]