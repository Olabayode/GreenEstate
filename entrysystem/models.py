from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, username, email, usertype, password, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")
        if other_fields.get("is_active") is not True:
            raise ValueError("Superuser must be assigned to is_active=True.")

        return self.create_user(username, email, usertype, password, **other_fields)

    def create_user(self, username, email, usertype, password, **other_fields):


        email = self.normalize_email(email)
        if not email:
            raise ValueError("You must provide an email address")
        user = self.model(
            username=username, email=email, usertype=usertype, **other_fields
        )
        user.set_password(password)
        user.save()

        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    admin = "admin"
    resident = "resident"
    security = "security"
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField("email address", unique=True)
    user_type = [(admin, "Admin"), (resident, "Resident"), (security, "Security")]
    usertype = models.CharField(
        max_length=20,
        choices=user_type,
        default=admin,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "usertype"]

    def __str__(self):
        return self.username


class AdminManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(usertype=NewUser.admin)


class Admin(NewUser):
    base_usertype = NewUser.admin

    admin = AdminManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for admin"


class AdminProfile(models.Model):
    objects = None
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    admin_id = models.IntegerField(null=True, blank=True)


class ResidentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(usertype=NewUser.resident)


class Resident(NewUser):
    base_usertype = NewUser.resident

    resident = ResidentManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for residents"


class ResidentProfile(models.Model):
    objects = None
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    resident_id = models.IntegerField(null=True, blank=True)


class SecurityManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(usertype=NewUser.security)


class Security(NewUser):
    base_usertype = NewUser.security

    security = SecurityManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for securities"


class SecurityProfile(models.Model):
    objects = None
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    security_id = models.IntegerField(null=True, blank=True)


class Visitor(models.Model):
    name = models.CharField(max_length=150, unique=False)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    code = models.CharField(max_length=6, unique=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
