from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = self.normalize_email(email),
        )
        print('password', password)
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = self.normalize_email(email),
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=100)
    last_name       = models.CharField(max_length=100)
    username        = models.CharField(max_length=100, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=100)

    country = models.CharField(blank=True, max_length=100)
    state = models.CharField(blank=True, max_length=100)
    city = models.CharField(blank=True, max_length=100)
    address = models.CharField(blank=True, max_length=100)
    zip_code = models.CharField(blank=True, max_length=100)

    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = AccManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

