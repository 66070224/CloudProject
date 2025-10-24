from django.shortcuts import render
from rest_framework.views import APIView
from courses.models import Course
from django.http import Http404
from courses.serializers import CourseSerializer
from rest_framework.response import Response

# Create your views here.
class CourseDetail(APIView):

    def get_object(self, code):
        try:
            return Course.objects.get(code=code)
        except Course.DoesNotExist:
            return Http404

    def get(self, request, code):
        course = self.get_object(code)
        serializer = CourseSerializer(course)
        return Response(serializer.data)