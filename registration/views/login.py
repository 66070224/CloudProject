from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from registration.forms import *

# Cognito
from ..services.cognito import get_user, login_cognito, change_password_cognito

# ระบบ Login
class LoginView(View):
    # แสดงหน้า Login
    def get(self, request):
        # เช็คว่า Redirect มาจาก method POST หรือไม่
        post = request.session.pop("post_login", False)
        error = request.session.pop("error", "")
        form = LoginForm(post) if post else LoginForm()
        
        print(f"{request.session.get('user_email')} is on.")
        return render(request, "login/login.html", context={
            "form": form, "error": error
        })
    
    # Login logic
    def post(self, request):
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            is_remember = form.cleaned_data.get("remember_me")
            print(f"remember: {is_remember}")
            
            # ส่งข้อมูลสำหรับ Login ไปยัง Cognito service
            login_result = login_cognito(email, password)
            response = redirect("login_view")
            
            # กรณี login สำเร็จปกติ
            if 'AuthenticationResult' in login_result:
                idToken = login_result['AuthenticationResult']['IdToken']
                self.user, self.role = get_user(idToken)
                
                self.login(request)

                # ถ้าติ๊ก จดจำฉัน
                if is_remember: 
                    refreshToken = login_result['AuthenticationResult']['RefreshToken']
                    response.set_cookie(
                        "refresh_token",
                        refreshToken,
                        httponly=True,
                        secure=False, # สำหรับ Dev เท่านั้น
                        max_age=30*24*60*60 # 30
                    )
                
                return response
                
            # กรณี user ต้องเปลี่ยนรหัสผ่าน
            elif login_result.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
                request.session["email"] = email
                request.session["session"] = login_result['Session']
                return redirect("change_password_view")
            
            # กรณีที่ข้อมูลไม่ถูกต้อง
            else:
                request.session["error"] = login_result["message"]
                return response

        # กรณี Form ไม่ valid จะส่งแจ้งข้อมูลผิดพลาดกลับไป
        request.session["post_login"] = request.POST
        return redirect("login_view")

    # Function สำหรับทำการ login โดยจะเก็บ session ไว้
    def login(self, request):
        print(self.user.email)
        request.session["user_email"] = self.user.email
        request.session["user_role"] = self.role
  

# สำหรับเปลี่ยนรหัส ในกรณีที่ User : FORCE_CHANGE_PASSWORD
class ChangePasswordView(View):
    # แสดงหน้าสำหรับเปลี่ยนรหัสผ่าน
    def get(self, request):
        # เช็คว่า Redirect มาจาก method POST หรือไม่
        post = request.session.pop("post_change_password", False)
        form = ChangePasswordFirstTimeForm(post) if post else ChangePasswordFirstTimeForm()

        return render(request, "login/change_password.html", context={
            "form": form,
        })

    # Logic สำหรับเปลี่ยนรหัส
    def post(self, request):
        email = request.session.pop("email", None) # ดึงข้อมูลจาก session แล้วลบ session นั้นออกเลย
        session = request.session.pop("session", None)
        form = ChangePasswordFirstTimeForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data.get("password")
            # ส่งข้อมูลสำหรับเปลี่ยนรหัสไป Cognito service
            change_password_result = change_password_cognito(request, email, new_password, session)

            print(f"Change {email}'s password successfully.")
            return redirect("login_view")

        # กรณี Form ไม่ valid จะส่งแจ้งข้อมูลผิดพลาดกลับไป
        request.session["email"] = email
        request.session["session"] = session
        request.session["post_change_password"] = request.POST
        return redirect("change_password_view")

class LogoutView(View):
    def get(self, request):
        print(f'{request.session.get("user_email")} logout.')
        request.session.flush() # ลบทุก Session

        return redirect('login_view')