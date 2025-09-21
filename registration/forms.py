from django import forms
from django.forms import ModelForm, Form, ValidationError
from .validators import validate_password_strength

class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={
            "class": "mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3"
        })
    )
    password = forms.CharField(
        required=True,
        validators=[validate_password_strength],
        widget=forms.PasswordInput(attrs={
            "class": "mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3 pr-12",
            "id": "password"
        },)
    )
    remember_me = forms.BooleanField(required=False)

    # Validation เฉพาะ field Email
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@test.ac.th"):
            raise ValidationError("ต้องใช้ @test.ac.th เท่านั้น")
        
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password or password.strip() == "":
            raise ValidationError("กรุณากรอกรหัสผ่าน")
        
        return password

class ChangePasswordFirstTimeForm(forms.Form):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "class": "mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3 pr-12",
            "id": "password"
        })
    )
    confirmed_password = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={
            "class": "mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-3 pr-12",
            "id": "confirmed_password"
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmed_password = cleaned_data.get("confirmed_password")
        
        validate_password_strength(password) # ตรวจสอบรหัสผ่านว่ามีอักขระตามที่ Cognito กำหนดหรือไม่
        
        if password != confirmed_password:
            raise ValidationError("รหัสผ่านไม่ตรงกัน")
        
        return cleaned_data