from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

from departments.models import Department, Faculty

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "adm")

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    title = models.CharField(max_length=10)
    class RoleChoices(models.TextChoices):
        STUDENT = "stu", _("Student")
        PROFESSOR = "pro", _("Professor")
        REGISTRA = "reg", _("Registra")
        ADMIN = "adm", _("Admin")
    role = models.CharField(max_length=3, choices=RoleChoices.choices, default=RoleChoices.STUDENT)
    img = models.ImageField(upload_to='profile_images/')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def is_student(self):
        return self.role == self.RoleChoices.STUDENT

    @property
    def is_professor(self):
        return self.role == self.RoleChoices.PROFESSOR

    @property
    def is_registra(self):
        return self.role == self.RoleChoices.REGISTRA

    @property
    def is_admin(self):
        return self.role == self.RoleChoices.ADMIN
    
    @property
    def get_full_name_with_title(self):
        return f"{self.title} {self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.email}"
