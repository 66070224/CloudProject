import re
from django.core.exceptions import ValidationError

def validate_password_strength(value):
    if len(value) < 8:
        raise ValidationError("รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร")
    if not re.search(r"[A-Z]", value):
        raise ValidationError("รหัสผ่านต้องมีตัวอักษรพิมพ์ใหญ่อย่างน้อย 1 ตัว")
    if not re.search(r"[a-z]", value):
        raise ValidationError("รหัสผ่านต้องมีตัวอักษรพิมพ์เล็กอย่างน้อย 1 ตัว")
    if not re.search(r"[0-9]", value):
        raise ValidationError("รหัสผ่านต้องมีตัวเลขอย่างน้อย 1 ตัว")
    if not re.search(r"[_!@#$%^&*(),.?\":{}|<>\[\]]", value):
        raise ValidationError("รหัสผ่านต้องมีอักขระพิเศษอย่างน้อย 1 ตัว")
