from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from courses.models import Course
from django.http import Http404
from courses.serializers import CourseSerializer
from rest_framework.response import Response
from personnels.models import Professor

# Create your views here.
class CourseDetailAPI(APIView):

    def get_object(self, code):
        try:
            return Course.objects.get(code=code)
        except Course.DoesNotExist:
            return Http404

    def get(self, request, code):
        course = self.get_object(code)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

class MyCourseView(View):
    def get(self, request):
        professor = Professor.objects.get(user_id=request.user.id)
        courses = Course.objects.filter(professors=professor)
        return render(request, "courses/professor/course.html", {"courses": courses})