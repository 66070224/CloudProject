from django.urls import path
from enrollments.views import IndexView, EnrollView, SubmitAPI, EnrollListView, ConfirmAPI, EnrollGradeView

urlpatterns = [
    path('', IndexView.as_view(), name="enroll_index"),
    path('enroll', EnrollView.as_view(), name="enroll_enroll"),
    path('enrolllist', EnrollListView.as_view(), name="enroll_enrolllist"),

    path('grade/<int:id>', EnrollGradeView.as_view(), name="grade"),

    path('api/submit/<str:courses>', SubmitAPI.as_view(), name="api_submit"),
    path('api/Confirm/<int:id>/<str:text>', ConfirmAPI.as_view(), name="api_confirm"),
]