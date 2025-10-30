import jwt, boto3
from django.conf import settings
from django_cognito_jwt.validator import TokenValidator, TokenError
from types import SimpleNamespace
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from botocore.exceptions import ClientError

# Models
from .models import *

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
        self.ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
        self.SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
        self.SESSION_TOKEN = settings.AWS_SESSION_TOKEN
        self.client = boto3.client('cognito-idp', 
                                   region_name=self.CLIENT_REGION,
                                   aws_access_key_id=self.ACCESS_KEY_ID,
                                   aws_secret_access_key=self.SECRET_ACCESS_KEY,
                                   aws_session_token=self.SESSION_TOKEN,
                                   )

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
        from datetime import datetime, timezone, timedelta
        try:
            # decode token แบบไม่ verify
            unverified_claims = jwt.decode(id_token, options={"verify_signature": False})
            iat = unverified_claims.get("iat")
            if iat:
                token_time = datetime.fromtimestamp(iat, tz=timezone.utc)
                now = datetime.now(timezone.utc)
                # ยอมเวลา skew 60 วินาที
                if now + timedelta(seconds=60) < token_time:
                    print("Token not yet valid")
                    return None, None

            # validate token จริง
            claims = self.validator.validate(id_token)
        except TokenError as e:
            print(f"Token validation error: {str(e)}")
            return None, None
        
        email = claims.get("email")
        groups = claims.get("cognito:groups", [])

        group = groups[0] if groups else None
        return email, group


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
            )
            self.client.admin_set_user_password(
                UserPoolId=self.USER_POOL_ID,
                Username=email,
                Password=password,
                Permanent=True
            )
            return {"message": "Create successed.", "status": True}
        except self.client.exceptions.UsernameExistsException:
            return {'message': "Username is already exist.", "status": False}
    
    def update_user_email_cognito(self, email, new_email):
        try:
            response = self.client.admin_update_user_attributes(
                UserPoolId=self.USER_POOL_ID,
                Username=email,
                UserAttributes=[
                    {'Name': 'email', 'Value': new_email},
                    {'Name': 'email_verified', 'Value': 'true'}  # ถ้าไม่ต้องการให้ผู้ใช้ verify ใหม่
                ]
            )
            return True
        except ClientError as e:
            print(f"Failed to update email: {e}")
            return False

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