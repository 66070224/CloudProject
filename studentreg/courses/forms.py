from django.forms import ModelForm

from courses.models import Course, Section, Class

class CourseForm(ModelForm):
    class Meta():
        model = Course
        fields = '__all__'

class SectionForm(ModelForm):
    class Meta():
        model = Section
        fields = '__all__'

class ClassForm(ModelForm):
    class Meta():
        model = Class
        fields = '__all__'