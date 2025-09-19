import boto3
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from registration.forms import *

# สร้าง client ของ Cognito
client = boto3.client('cognito-idp', region_name=settings.COGNITO_REGION)
# Set Cognito จาก settings
USER_POOL_ID = settings.COGNITO_USER_POOL_ID
CLIENT_ID = settings.COGNITO_APP_CLIENT_ID
CLIENT_SECRET = settings.COGNITO_APP_CLIENT_SECRET

# สำหรับ Client Secret
import hmac
import hashlib
import base64
def get_secret_hash(email):
    message = email + CLIENT_ID
    dig = hmac.new(
        key=bytes(CLIENT_SECRET, 'utf-8'),
        msg=bytes(message, 'utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()

# สำหรับตรวจสอบ Role
def is_student(id_token):
    import jwt
    decoded = jwt.decode(id_token, options={"verify_signature":False})
    groups = decoded.get("cognito:groups", [])
    
    return "Student" in groups

# ระบบ Login
class LoginView(View):
    # แสดงหน้า Login
    def get(self, request):
        # เช็คว่า Redirect มาจาก method POST หรือไม่
        post = request.session.pop("post_login", None) or False
        if post:
            form = LoginForm(post, initial={"email": post})
        else:
            form = LoginForm()
        
        return render(request, "login/login.html", context={
            "form": form,
        })
    
    # Login logic
    def post(self, request):
        form = LoginForm(request.POST)
        
        try:
            if form.is_valid():
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password")
                
                # ส่งข้อมูลสำหรับ Login ไปยัง Cognito service
                response = client.initiate_auth(
                    ClientId=CLIENT_ID,
                    AuthFlow='USER_PASSWORD_AUTH',
                    AuthParameters={
                        'USERNAME': email,
                        'PASSWORD': password,
                        'SECRET_HASH': get_secret_hash(email) # ส่ง secret hash ไปเพื่อยืนยันตัวตน
                    }
                )
                
                # กรณี login สำเร็จปกติ
                if 'AuthenticationResult' in response:
                    idToken = response['AuthenticationResult']['IdToken']
                    if is_student(idToken):
                        from ..models import Student
                        student = Student.objects.get(email=email)

                        request.session["user"] = student
                    else:
                        return JsonResponse({'status': 'success', 'message': 'You are staff.'})
                    
                    return JsonResponse({'Role': 'Staff', 'message': response})

                # กรณี user ต้องเปลี่ยนรหัสผ่าน
                elif response.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
                    request.session["email"] = email
                    request.session["session"] = response['Session']
                    return redirect("change_password_view")
                else:
                    return JsonResponse({'status': 'error', 'message': 'Unknown authentication challenge'})

            request.session["post_login"] = request.POST
            return redirect("login_view")

        except client.exceptions.NotAuthorizedException:
            return JsonResponse({'status': 'error','message':'Incorrect username or password'})
        except client.exceptions.UserNotConfirmedException:
            return JsonResponse({'status': 'error','message':'User not confirmed'})
        
        

# สำหรับเปลี่ยนรหัส ในกรณีที่ User : FORCE_CHANGE_PASSWORD
class ChangePasswordView(View):
    # แสดงหน้าสำหรับเปลี่ยนรหัสผ่าน
    def get(self, request):
        # เช็คว่า Redirect มาจาก method POST หรือไม่
        post = request.session.pop("post_change_password", None) or False
        if post:
            form = ChangePasswordFirstTimeForm(post)
        else:
            form = ChangePasswordFirstTimeForm()

        return render(request, "login/change_password.html", context={
            "form": form,
        })

    # Logic สำหรับเปลี่ยนรหัส
    def post(self, request):
        email = request.session.pop("email", None) # ดึงข้อมูลจาก session แล้วลบ session นั้นออกเลย
        session = request.session.pop("session", None)
        form = ChangePasswordFirstTimeForm(request.POST)

        print(email)
        try:
            if form.is_valid():
                new_password = form.cleaned_data.get("password")
                # ส่งข้อมูลสำหรับเปลี่ยนรหัสไป Cognito service
                response = client.respond_to_auth_challenge(
                    ClientId=CLIENT_ID,
                    ChallengeName='NEW_PASSWORD_REQUIRED',
                    Session=session,
                    ChallengeResponses={
                        'USERNAME': email,
                        'NEW_PASSWORD': new_password,
                        'SECRET_HASH': get_secret_hash(email)
                    }
                )

                # สร้างข้อมูลเบื้องต้นสำหรับนักศึกษา
                from ..models import Student
                Student.objects.create(
                    email=email,
                    code=email.strip("@")[0]
                )

                return redirect("login_view")

            request.session["email"] = email
            request.session["session"] = session
            request.session["post_change_password"] = request.POST
            return redirect("change_password_view")

        except Exception as e:
            request.session["email"] = email
            request.session["session"] = session
            return JsonResponse({'status': 'error', 'message': f"{str(e)}"})

