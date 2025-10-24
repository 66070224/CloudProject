from django.urls import path
from enrollments.views import IndexView, EnrollView, SubmitView, EnrollListView

urlpatterns = [
    path('', IndexView.as_view(), name="enroll_index"),
    path('enroll', EnrollView.as_view(), name="enroll_enroll"),
    path('enrolllist', EnrollListView.as_view(), name="enroll_enrolllist"),
    path('api/submit/<str:courses>', SubmitView.as_view(), name="api_submit"),
]