from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, get_user, update_session_auth_hash
from django.urls import reverse
from accounts.models import CustomUser
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from .services import CognitoService

cognito = CognitoService()

# Create your views here.
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("home"))
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("home"))
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            login_result = cognito.login_cognito(email=email, password=password)

            if 'AuthenticationResult' in login_result:
                request.session["AccessToken"] = login_result["AuthenticationResult"]["AccessToken"]
                request.session["RefreshToken"] = login_result["AuthenticationResult"]["RefreshToken"]
                request.session["IdToken"] = login_result["AuthenticationResult"]["IdToken"]
                user = form.get_user()
                login(request, user)
                return redirect(reverse("home"))
        return render(request, 'login.html', {"form": form})

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(reverse("login"))
    
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_student:
            enrolls = request.user.student.enrolls.select_related('section__course').all()
            return render(request, 'profile.html', {'enrolls': enrolls})

        return render(request, 'profile.html')

class ChangePassword(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'changepassword.html', { "form": form })
    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'เปลี่ยนรหัสผ่านเรียบร้อยแล้ว!')
            return redirect(reverse("profile"))
        messages.error(request, 'โปรดตรวจสอบข้อมูลอีกครั้ง')
        return render(request, 'changepassword.html', {'form': form})