from rest_framework import serializers
from .models import *
from rest_framework.serializers import Serializer
from rest_framework.fields import CharField, IntegerField, DateTimeField, BooleanField, UUIDField



class UserPaymentDetailSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = UserPaymentDetail
        fields = '__all__'
class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = UserSubscription
        fields = '__all__'
class UserBonusSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = UserBonus
        fields = '__all__'


class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = SubscriptionLookUpModel
        fields = '__all__'