from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager


transactions = [
    ["cash_out", "Cash Out"],
    ["cash_in", "Cash In"]
]

class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

class Country(models.Model):
    name = models.CharField(max_length=200, unique="True")

    def __str__(self): 
        return self.name

class Institution(models.Model):
    name = models.CharField(max_length=300, unique=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    name = models.CharField(max_length=200);

    def __str__(self):
        return self.name

class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.code

class GeneralAccount(models.Model):
    amount = models.BigIntegerField();

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    amount = models.BigIntegerField(default=0)
    transaction_type = models.CharField(choices=transactions, max_length=15)

class ForgotPasswordToken(models.Model):
    email = models.EmailField()
    secret_token = models.CharField(max_length=124)