from rest_framework import serializers
from user_management.models import User, otpLogin, Profile
from subscription.models import *
from .models import CompanyInfo
from rest_framework.fields import CharField, IntegerField, DateTimeField, BooleanField, UUIDField

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class AdminDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']

class AdminLoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    admin_details = AdminDetailSerializer()

#new
class UserActivationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    flag = serializers.BooleanField()


class UserActivationResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


#req 2
class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)
    username = serializers.CharField(required=False)



    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'first_name', 'last_name']




#req3
class UserCountSerializer(serializers.Serializer):
    
    active_users = serializers.IntegerField(required=False)
    non_active_users = serializers.IntegerField(required=False)
    total_users = serializers.IntegerField(required=False)
    total_admins = serializers.IntegerField(required=False)


#req 6


#req7


class UserSearchResultSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)
    first_name= serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)


    class Meta:
        model = User

        fields = ('id', 'username', 'email', 'phone_number', 'first_name', 'last_name')



# req8
class SingleUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    last_name= serializers.CharField(required=False)
    email = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'first_name', 'last_name')

#req 4

class TopEarningUserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(required=False)
    email = serializers.SerializerMethodField(required=False)

    class Meta:
        model = UserBonus
        fields = ['user_id', 'balance', 'username', 'email']

    def get_username(self, obj):
        try:
            user = User.objects.get(id=obj.user_id)
            return user.username
        except User.DoesNotExist:
            return ''

    def get_email(self, obj):
        try:
            user = User.objects.get(id=obj.user_id)
            return user.email
        except User.DoesNotExist:
            return ''

#req 5 Get balance
class ActiveUsersBalanceSerializer(serializers.Serializer):

    total_active_users_balance = serializers.DecimalField(max_digits=10, decimal_places=2,required=False)

#req 5.1 Get company earning

class CompanyInfoSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(required=False)
    description = serializers.SerializerMethodField(required=False)
    total_revenue = serializers.SerializerMethodField(required=False)
    month_name = serializers.SerializerMethodField(required=False)
    year_name= serializers.SerializerMethodField(required=False)
    class Meta:
        model = CompanyInfo
        fields = '__all__'

    def get_name(self, obj):
        return obj.name

    def get_description(self, obj):
        return obj.description

    def get_total_revenue(self, obj):
        return obj.total_revenue

    def get_month_name(self, obj):
        return obj.month_name

    def get_year_name(self, obj):
        return obj.year_name


# req 12 Add Revenue
class AddRevenueSerializer(serializers.Serializer):
    revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    month_name = serializers.CharField(max_length=255)
    year_name = serializers.CharField(max_length=4)



#req Date Filtered Active/nonactive users list
class DateFilteredUserCountSerializer(serializers.Serializer):
    active_users = serializers.IntegerField(required=False)
    non_active_users = serializers.IntegerField(required=False)
    total_users = serializers.IntegerField(required=False)

