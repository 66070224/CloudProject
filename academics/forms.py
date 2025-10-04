from django import forms
from django.forms import widgets, ModelForm
from .models import *

FORM_INPUT = "bg-transparent border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"

class CourseForm(ModelForm):
    class Meta:
        model=Course
        fields='__all__'
        widgets={
            "code": widgets.TextInput(attrs={"class": FORM_INPUT,}),
            "name": widgets.TextInput(attrs={"class": FORM_INPUT,}),
            "credits": widgets.NumberInput(attrs={"class": FORM_INPUT,}),
            "department": widgets.Select(attrs={"class": FORM_INPUT,}),
        }

class SectionForm(ModelForm):
    class Meta:
        model=CourseSection
        fields='__all__'
        widgets={
            "course": widgets.Select(attrs={"class": FORM_INPUT,}),
            "section_number": widgets.NumberInput(attrs={"class": FORM_INPUT,}),
            "professor": widgets.Select(attrs={"class": FORM_INPUT,}),
            "class_type": widgets.Select(attrs={"class": FORM_INPUT,}),
            "day": widgets.Select(attrs={"class": FORM_INPUT,}),
            "start_time": widgets.TimeInput(attrs={"class": FORM_INPUT, "type": "time"}),
            "end_time": widgets.TimeInput(attrs={"class": FORM_INPUT, "type": "time"}),
            "location": widgets.TextInput(attrs={"class": FORM_INPUT,}),
            "capacity": widgets.NumberInput(attrs={"class": FORM_INPUT,}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ถ้ามี course อยู่แล้ว (จาก instance หรือ initial data)
        course = None
        if self.instance and self.instance.course_id:
            course = self.instance.course
        elif "course" in self.data:  # ใช้ตอน POST
            try:
                course = Course.objects.get(pk=self.data.get("course"))
            except Course.DoesNotExist:
                pass

        if course:
            self.fields["professor"].queryset = Professor.objects.filter(department=course.department)
        else:
            # ยังไม่เลือก course ให้ queryset ว่างๆ ไปก่อน
            self.fields["professor"].queryset = Professor.objects.none()

class DepartmentForm(ModelForm):
    class Meta:
        model=Department
        fields='__all__'
        widgets={
            "name": widgets.TextInput(attrs={"class": FORM_INPUT,}),
            "faculty": widgets.Select(attrs={"class": FORM_INPUT,}),
            "term_fees": widgets.NumberInput(attrs={"class": FORM_INPUT,}),
        }
    
class ProfessorForm(ModelForm):
    class Meta:
        model=Professor
        fields='__all__'
        widgets={
            "first_name": widgets.TextInput(attrs={"class": FORM_INPUT,}),
            "last_name": widgets.TextInput(attrs={"class": FORM_INPUT,}),
            "department": widgets.Select(attrs={"class": FORM_INPUT,}),
        }