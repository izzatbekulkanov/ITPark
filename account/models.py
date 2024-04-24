from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUserManager(BaseUserManager):
    """Define a model manager for CustomUser model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a CustomUser with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# Create your models here.


class CustomUser(AbstractUser):
    type_choice = (
        ("1", "Erkak"),
        ("2", "Ayol"),
    )
    username = models.CharField(null=True, blank=True, max_length=9, unique=True)
    email = models.EmailField(('email address'), unique=True)
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="To'liq ism")
    short_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="Qisqa ism")
    first_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="Ism")
    second_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="Familia")
    third_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="Otasining ismi")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan kun")
    image = models.URLField(blank=True, null=True, max_length=255, verbose_name="Rasm")

    imageFile = models.ImageField(upload_to='students/%Y/%m/%d', verbose_name="Rasmi faylda", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqti")
    now_role = models.CharField(null=True, blank=True, max_length=255, verbose_name="Foydalanuvchining hozirgi vaqtdagi roli")
    age = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(null=True, max_length=15, blank=True)
    gender = models.CharField(_('Jinsi'), choices=type_choice, default="1", max_length=20, blank=True, null=True)
    is_employee = models.BooleanField(default=False, verbose_name="Hodim" , blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # Additional fields for the university
    passport_serial = models.CharField(max_length=20, null=True, blank=True)
    passport_issue_date = models.DateField(null=True, blank=True)
    passport_jshshir = models.CharField(max_length=20, null=True, blank=True)
    #Ijtimoiy tarmoqlar

    telegram = models.URLField(null=True, blank=True, verbose_name="Telegram profil havolasi")
    instagram = models.URLField(null=True, blank=True, verbose_name="Instagram profil havolasi")
    facebook = models.URLField(null=True, blank=True, verbose_name="Facebook profil havolasi")


    def __str__(self):
        return self.username  # yoki return self.email yoki return self.full_name


    USERNAME_FIELD = 'email'  # Users login in with their email
    REQUIRED_FIELDS = ['username']  # username required field
