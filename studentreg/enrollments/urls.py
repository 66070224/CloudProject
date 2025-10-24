from django.urls import path
from enrollments.views import IndexView, EnrollView, SubmitView

urlpatterns = [
    path('', IndexView.as_view(), name="enroll_index"),
    path('enroll', EnrollView.as_view(), name="enroll_enroll"),
    path('api/submit/<str:courses>', SubmitView.as_view(), name="api_submit"),
]