from django.forms import ModelForm
from personnels.models import Student, Professor, Registra
from accounts.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomerUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["email", "title", "first_name", "last_name"]

class StudentForm(ModelForm):
    class Meta():
        model = Student
        fields = ["student_id", "department", "year"]

class ProfessorForm(ModelForm):
    class Meta():
        model = Professor
        fields = ["department"]

class RegistraForm(ModelForm):
    class Meta():
        model = Registra
        fields = ["faculty"]