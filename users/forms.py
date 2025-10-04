from django import forms
from django.forms import widgets, ModelForm
from .models import *

FORM_INPUT = "bg-transparent border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"

class StudentForm(ModelForm):
    class Meta:
        model=Student
        fields=["first_name", "last_name", "email", "code", "department"]
        widgets={
            "first_name": widgets.TextInput(attrs={"class": FORM_INPUT,}),
            "last_name": widgets.TextInput(attrs={"class": FORM_INPUT,}),
            "email": widgets.EmailInput(attrs={"class": FORM_INPUT,}),
            "code": widgets.TextInput(attrs={"class": FORM_INPUT,}),
            "department": widgets.Select(attrs={"class": FORM_INPUT,}),
        }