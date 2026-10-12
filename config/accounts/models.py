from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.functions import Lower
# Create your models here.

class CustomUserManager(BaseUserManager):
    """Custom manager to handle email normalization and safe user creation."""

    def normalize_email(self, email):
        return super().normalize_email(email).lower()

    def create_user(self, username, email=None, password=None, **extra_fields):
        # Enforce safe default privileges for regular user creation
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "CUSTOMER")

        if email:
            email = self.normalize_email(email)
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Ensures Django handles password hashing
        user.save(using=self._db)
        return user
 
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if email:
            email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    class Role(models.TextChoices): 
        CUSTOMER = "CUSTOMER", "Customer"
        STAFF = "STAFF", "Staff" 
        ADMIN = "ADMIN", "Admin"
    email = models.EmailField(blank=False,unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER )
    objects = CustomUserManager()
    phone = models.CharField(max_length=20,blank=True,null=True)
    is_approved = models.BooleanField(default=False)
    class Meta: constraints = [ models.UniqueConstraint( 
        Lower("email"),
        name="unique_customuser_email_ci" ) ]

    def save(self, *args, **kwargs):
        # Normalize email to lowercase before saving
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)