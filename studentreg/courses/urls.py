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


    path('professor/course', MyCourseView.as_view(), name="mycourse"),
    path('api/detail/<str:code>', CourseDetailAPI.as_view(), name="api_coursedetail"),
]