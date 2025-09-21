from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login_view"),
    path("logout/", views.LogoutView.as_view(), name="logout_view"),
    path("change_password/", views.ChangePasswordView.as_view(), name="change_password_view"),
    path("registration/", views.RegistrationView.as_view(), name="registration_view"),
]