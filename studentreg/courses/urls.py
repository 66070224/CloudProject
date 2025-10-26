from django.urls import path
from courses.views import *

urlpatterns = [
    path('registra', RegistraIndexView.as_view(), name="course_registra"),

    path('registra/course', RegistraCourseView.as_view(), name="course_registra_courselist"),
    path('registra/course/create', CreateCourseView.as_view(), name="course_registra_create"),
    path('registra/course/edit/<int:id>', EditCourseView.as_view(), name="course_registra_edit"),

    path('registra/section', RegistraSectionView.as_view(), name="course_registra_sectionlist"),
    path('registra/section/create', CreateSectionView.as_view(), name="course_registra_sectioncreate"),
    path('registra/section/edit/<int:id>', EditSectionView.as_view(), name="course_registra_sectionedit"),

    path('registra/class', RegistraClassView.as_view(), name="course_registra_classlist"),
    path('registra/class/create', CreateClassView.as_view(), name="course_registra_classcreate"),
    path('registra/class/edit/<int:id>', EditClassView.as_view(), name="course_registra_classedit"),

    path('professor/course', ProfessorCourseView.as_view(), name="course_professor_courselist"),
    path('professor/course/detail/<int:id>', ProfessorCourseDetailView.as_view(), name="course_professor_coursedetail"),


    path('professor/section', ProfessorSectionView.as_view(), name="course_professor_sectionlist"),
    path('professor/section/detail/<int:id>', ProfessorSectionDetailView.as_view(), name="course_professor_sectiondetail"),


    path('api/detail/<str:code>', CourseDetailAPI.as_view(), name="api_coursedetail"),
]