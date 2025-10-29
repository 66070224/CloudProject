from rest_framework import serializers
from courses.models import Course, Section, Class
from enrollments.models import Enroll
from personnels.models import Professor
from accounts.models import CustomUser

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ["type", "day", "start_time", "end_time", "location"]

class EnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enroll
        fields = "__all__"

class SectionSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True)
    enrolls = EnrollSerializer(many=True)
    class Meta:
        model = Section
        fields = ["number", "capacity", "classes", "enrolls"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["title", "first_name", "last_name"]

class ProfessorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Professor
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    professors = ProfessorSerializer(many=True)
    sections = SectionSerializer(many=True)

    class Meta:
        model = Course
        fields = "__all__"