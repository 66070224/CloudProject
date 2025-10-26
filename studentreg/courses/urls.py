from django.urls import path
from courses.views import *

urlpatterns = [
    path('', CourseIndexView.as_view(), name="course_index"),

    path('course', CourseListView.as_view(), name="course_course_list"),
    path('course/create', CreateCourseView.as_view(), name="course_course_create"),
    path('course/edit/<int:id>', EditCourseView.as_view(), name="course_course_edit"),

    path('section', SectionListView.as_view(), name="course_section_list"),
    path('section/create', CreateSectionView.as_view(), name="course_section_create"),
    path('section/edit/<int:id>', EditSectionView.as_view(), name="course_section_edit"),

    path('class', ClassListView.as_view(), name="course_class_list"),
    path('class/create', CreateClassView.as_view(), name="course_class_create"),
    path('class/edit/<int:id>', EditClassView.as_view(), name="course_class_edit"),

    path('api/detail/<str:code>', CourseDetailAPI.as_view(), name="course_api_course_detail"),
]