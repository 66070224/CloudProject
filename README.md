ปัจจุบันเชื่อมแค่ RDS และ Cognito เท่านั้น
!! ถ้าจะ test โดยลองเชื่อมกับ aws ให้มาบอก เพื่อเปิด rds (ถ้าเปิดทิ้งวัน มันเปลืองเครดิต) !!

Lib ที่ต้องลง:
    - Cognito : pip install django-cognito-jwt

User:
    - email: admin@test.ac.th | password: Admin_12

การสร้าง View:
    - สร้างไฟล์ใน folder views แล้วไป import ใน __init__.py ใน folder views
    - เช่น ทำ View เกี่ยวกับการ login ไปสร้าง view ในไฟล์ views/login.py ซึ่งมี LoginView และ ChangePasswordView
