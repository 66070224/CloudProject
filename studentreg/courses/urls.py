from django.urls import path
from courses.views import CourseDetailAPI, MyCourseView

urlpatterns = [
    path('mycourse', MyCourseView.as_view(), name="mycourse"),
    path('api/detail/<str:code>', CourseDetailAPI.as_view(), name="api_coursedetail"),
]