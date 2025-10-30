# from django.contrib.auth import get_user_model
# from django.contrib.auth.backends import BaseBackend
# from django.conf import settings
# from .services import CognitoService

# User = get_user_model()

# class CognitoBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None):
#         cognito = CognitoService()
#         try:
#             # ลอง login กับ Cognito
#             auth_result = cognito.login(username, password)
#             if not auth_result:
#                 return None

#             # ถ้า Cognito login สำเร็จ ให้ดึง user จาก DB หรือสร้างใหม่
#             user, created = User.objects.get_or_create(email=username)
#             return user
#         except Exception:
#             return None

#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None
