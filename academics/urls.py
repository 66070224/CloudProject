from django.urls import path
from . import views

urlpatterns = [
    path("manage_course/", views.ManageCourseView.as_view(), name="manage_course_view"),
    path("manage_section/", views.ManageSectionView.as_view(), name="manage_section_view"),
    path("manage_department/", views.ManageDepartmentView.as_view(), name="manage_department_view"),
    path("manage_professor/", views.ManageProfessorView.as_view(), name="manage_professor_view"),
    path("edit_course/<course_code>", views.EditCourseView.as_view(), name="edit_course_view"),
    path("edit_section/<id>", views.EditSectionView.as_view(), name="edit_section_view"),
    path("edit_department/<id>", views.EditDepartmentView.as_view(), name="edit_department_view"),
    path("edit_professor/<id>", views.EditProfessorView.as_view(), name="edit_professor_view"),

    path("get_professors/", views.ManageSectionView.get_professors, name="get_professors"),
]
