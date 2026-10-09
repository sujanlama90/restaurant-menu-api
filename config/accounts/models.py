from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower
# Create your models here.

class CustomUser(AbstractUser):
    class Role(models.TextChoices): 
        CUSTOMER = "CUSTOMER", "Customer"
        STAFF = "STAFF", "Staff" 
        ADMIN = "ADMIN", "Admin"
    email = models.EmailField(blank=False,unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER )
    phone = models.CharField(max_length=20,blank=True,null=True)
    class Meta: constraints = [ models.UniqueConstraint( 
        Lower("email"),
        name="unique_customuser_email_ci" ) ]