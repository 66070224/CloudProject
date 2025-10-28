from django.urls import path
from accounts.views import LoginView, LogoutView, ProfileView, ChangePassword

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('changepassword/', ChangePassword.as_view(), name="changepassword"),
]