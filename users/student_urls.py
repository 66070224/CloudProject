from django.urls import path
from .views import *

urlpatterns = [
    path("profile/", StudentProfileView.as_view(), name='student_profile_view'),
]