from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, account_type=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, account_type=account_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, account_type=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, password, account_type, **extra_fields)

    def create_superuser(self, email, password=None, account_type=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, account_type, **extra_fields)


class Owner(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    TYPES = (
        ('0', 'Admin'),
        ('1', 'Manager'),
        ('2', 'Staff'),
    )

    account_type = models.CharField(
        max_length=2,
        choices=TYPES,
        default='1',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['account_type']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # assigning user to group
        if self._state.adding:
            pass
        super(Owner, self).save(*args, **kwargs)
