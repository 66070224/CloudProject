from django.forms import ModelForm
from personnels.models import Student, Professor, Registra, Payment
from accounts.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomerUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["email", "title", "first_name", "last_name", "img"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["img"].required = True

class EditCustomerUserForm(UserChangeForm):
    password = None
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ["email", "title", "first_name", "last_name", "img"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["img"].required = True

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

class PayForm(ModelForm):
    class Meta():
        model = Payment
        fields = ["slip"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slip"].required = True