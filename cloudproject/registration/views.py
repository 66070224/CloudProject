from django.views import View
from django.shortcuts import render, redirect
from .models import Course
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View):
    def get(self, request):
        user = request.user
        context = {user: user}
        return render(request, "home.html", context)

class RegistrationView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        courses = Course.objects.all()
        context = {'courses': courses}
        return render(request, "registration.html", context)
    def post(self, request):
        
        pass

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, "login.html")

@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('login')