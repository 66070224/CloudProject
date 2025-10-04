import jwt, boto3
from django.conf import settings
from django_cognito_jwt.validator import TokenValidator
from types import SimpleNamespace
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from botocore.exceptions import ClientError

# Models
from users.models import *

# Lib สำหรับ Client Secret
import hmac
import hashlib
import base64

class CognitoService():
    
    def __init__(self):
        self.USER_POOL_ID = settings.COGNITO_USER_POOL_ID
        self.CLIENT_ID = settings.COGNITO_APP_CLIENT_ID
        self.CLIENT_SECRET = settings.COGNITO_APP_CLIENT_SECRET
        self.CLIENT_REGION = settings.COGNITO_REGION
        self.client = boto3.client('cognito-idp', region_name=self.CLIENT_REGION)

        # สร้าง validator สำหรับตรวจสอบ Token จาก Cognito
        self.validator = TokenValidator(
            aws_region=self.CLIENT_REGION,
            aws_user_pool=self.USER_POOL_ID,
            audience=self.CLIENT_ID
        )

    # สำหรับ Client Secret
    def get_secret_hash(self, email):
        message = email + self.CLIENT_ID
        dig = hmac.new(
            key=bytes(self.CLIENT_SECRET, 'utf-8'),
            msg=bytes(message, 'utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode()

    # รับข้อมูลผู้ใช้ โดยเช็ค groups ก่อน (ผ่าน JWT)
    def get_user(self, id_token):
        claims = self.validator.validate(id_token)
        email = claims.get("email")
        groups = claims.get("cognito:groups", [])

        if "Student" in groups:
            user, created = Student.objects.get_or_create(email=email, defaults={"email": email})
            # create เป็น boolean บอกว้า user ถูกสร้างหรือไม่
        else:
            user = SimpleNamespace(email=email, name="hello")
            print(user.name)

        group = groups[0] if groups else None
        return user, group


    def login_cognito(self, email, password):
        try:
            return self.client.initiate_auth(
                ClientId=self.CLIENT_ID,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password,
                    'SECRET_HASH': self.get_secret_hash(email) # ส่ง secret hash ไปเพื่อยืนยันตัวตน
                }
            )

        except self.client.exceptions.NotAuthorizedException:
            return {'message': "Email หรือ Password ไม่ถูกต้อง",}
        except self.client.exceptions.UserNotConfirmedException:
            return {'message': "User not confirmed",}

    def create_user_cognito(self, email, password):
        try:
            self.client.admin_create_user(   
                UserPoolId=self.USER_POOL_ID,
                Username=email,
                UserAttributes=[
                    {"Name": "email", "Value": email},
                    {"Name": "email_verified", "Value": "True"}
                ],
                TemporaryPassword=password,
                MessageAction="SUPPRESS",  # ไม่ส่งอีเมล
                DesiredDeliveryMediums=["EMAIL"]
            )
            return {"message": "Create successed."}
        except self.client.exceptions.UsernameExistsException:
            return {'message': "Username is already exist."}

    def change_password_cognito(self, request, email, password, session):
        try:
            response = self.client.respond_to_auth_challenge(
                ClientId=self.CLIENT_ID,
                ChallengeName='NEW_PASSWORD_REQUIRED',
                Session=session,
                ChallengeResponses={
                    'USERNAME': email,
                    'NEW_PASSWORD': password,
                    'SECRET_HASH': self.get_secret_hash(email)
                }
            )
            return response

        # กรณีเกิด Error อื่นๆ จะเก็บข้อมูลที่ใช้สำหรับแก้รหัสไว้อยู่
        except Exception as e:
            request.session["email"] = email
            request.session["session"] = session
            return JsonResponse({'status': 'error', 'message': f"{str(e)}"})
