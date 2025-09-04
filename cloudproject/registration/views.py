from django.views import View
from django.shortcuts import render
from .models import Course

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, "home.html")
    
class RegistrationView(View):
    def get(self, request):
        courses = Course.objects.all()
        context = {'courses': courses}
        return render(request, "registration.html", context)
    def post(self, request):
        
        pass

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")