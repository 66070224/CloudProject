from django.urls import path, include

from . import views

urlpatterns = [
    # Authen
    path("login/", views.LoginView.as_view(), name="login_view"),
    path("logout/", views.LogoutView.as_view(), name="logout_view"),
    path("change_password/", views.ChangePasswordView.as_view(), name="change_password_view"),
]