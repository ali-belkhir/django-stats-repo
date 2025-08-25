from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    QUALITY_CHOICES = (
        ("staff", "staff"),
        ("insurer", "insurer"),
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_quality = models.CharField(max_length=20, choices=QUALITY_CHOICES)
    insurance_name = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.user_quality == "staff":
            self.insurance_name = None
        super().save(*args, **kwargs)

    def clean(self):
        if self.user_quality == "insurer" and not self.insurance_name:
            raise ValidationError("Insurance name is required when quality is insurer.")
        if self.user_quality == "staff" and self.insurance_name:
            raise ValidationError("Staff users cannot have an insurance name.")

    def __str__(self):
        return f'Name: {self.first_name}, Quality: {self.user_quality}'
