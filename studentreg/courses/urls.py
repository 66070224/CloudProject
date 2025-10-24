from django.urls import path
from courses.views import CourseDetail

urlpatterns = [
    path('api/detail/<str:code>', CourseDetail.as_view(), name="api_coursedetail")
]