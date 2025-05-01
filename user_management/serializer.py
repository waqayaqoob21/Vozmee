from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import *
from rest_framework.serializers import Serializer
from rest_framework.fields import CharField, IntegerField, DateTimeField, EmailField
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'is_superuser', 'last_login',
                  'phone_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class OtpLoginSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = otpLogin
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        token['name'] = user.username
        return token


class ProfileSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Profile
        fields = ['country', 'email', 'full_name', 'username', 'gender', 'age', 'referral_code', 'phone_number']


# =========================Swagger Serlializers============================
class NewUserSerializer(Serializer):
    phone_number = IntegerField()
    username = CharField()
    email = EmailField()
    password = CharField()



class LoginUserSerializer(Serializer):
    username = CharField()
    password = CharField()


class LoginOtpSerializer(Serializer):
    otp = IntegerField()
    transaction_id = IntegerField()


class ForgetPasswordSerializer(Serializer):
    email = CharField()


class ResetPasswordSerializer(Serializer):
    password = CharField()


class EditProfile(Serializer):
    profile_picture = CharField(allow_null=True,allow_blank=True)
    first_name = CharField(allow_null=True,allow_blank=True)
    last_name = CharField(allow_null=True,allow_blank=True)
    phone_number = CharField(allow_null=True,allow_blank=True)
    country = CharField(allow_null=True,allow_blank=True)
    bio = CharField(allow_null=True,allow_blank=True)
    gender = CharField(allow_null=True,allow_blank=True)
    age = CharField(allow_null=True,allow_blank=True)

