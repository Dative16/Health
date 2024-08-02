from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
GENDER = [
    ('Female', 'Female'),
    ('Male', 'Male')
]


class MyAccountManager(BaseUserManager):

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, email, username, password=None):
        if not email:
            raise ValueError("User Must have an Email")
        if not username:
            raise ValueError("User Must have a Username")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=GENDER)
    age = models.IntegerField(default=0)
    date_of_birth = models.DateField(auto_now=True, null=True)
    date_of_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['first_name', 'username', 'last_name']
    USERNAME_FIELD = 'email'
    objects = MyAccountManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email

    def set_password_for_user(self, user, password):
        user.set_password(password)
        user.save()

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = 'Accounts'


class Patient(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    current_condition = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = 'Patients'


class HealthCareProvider(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    availability = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Health Care Provider"
        verbose_name_plural = 'Health Care Providers'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
