from django.urls import path
from enrollments.views import IndexView, EnrollView, SubmitAPI, EnrollListView, ConfirmAPI, GradeView, RefundAPI

urlpatterns = [
    path('', IndexView.as_view(), name="enrollment_index"),
    path('enrollment', EnrollView.as_view(), name="enrollment_enroll"),

    path('enroll', EnrollListView.as_view(), name="enrollment_enroll_list"),

    path('grade/<int:id>', GradeView.as_view(), name="enrollment_grade_edit"),

    path('api/submit/<str:courses>', SubmitAPI.as_view(), name="enrollment_api_submit"),
    path('api/Confirm/<int:id>/<str:text>', ConfirmAPI.as_view(), name="enrollment_api_confirm"),
    path('api/refund/<int:id>', RefundAPI.as_view(), name="enrollment_api_refund"),
]