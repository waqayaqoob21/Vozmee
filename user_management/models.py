from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=20)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()
class otpLogin(models.Model):
    id = models.AutoField(primary_key=True)
    otp = models.IntegerField()
    transaction_id = models.IntegerField()
    user_id = models.IntegerField(null=True)

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    profile_picture = models.CharField(max_length=1500, null=True)
    bio = models.CharField(max_length=500, null=True)
    country = models.CharField(max_length=300, null=True)
    gender = models.CharField(max_length=300, null=True)
    age = models.CharField(max_length=300, null=True)
    referral_code = models.CharField(max_length=300, null=True)
    user_id = models.IntegerField(null=True)
