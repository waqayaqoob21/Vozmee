from django.db import models

# Create your models here.
class UserPaymentDetail(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    is_payment = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(auto_now_add=False)
    amount  = models.IntegerField()
    referral_code = models.CharField(max_length=20)

class UserPaymentDetailHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    is_payment = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=False)
    expiry_date = models.DateTimeField(auto_now_add=False)
    amount  = models.IntegerField()
    referral_code = models.CharField(max_length=20)
    user_payment_id = models.IntegerField()

class UserSubscription(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    subscription_type_id = models.IntegerField()
    subscription_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True)

class UserSubscriptionHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    subscription_type_id = models.IntegerField()
    subscription_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False,null=True)
    user_subscription_id = models.IntegerField()

class UserBonus(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    balance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False,null=True)

class UserBonusHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    balance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False,null=True)
    user_bonus_id = models.IntegerField()


class SubscriptionLookUpModel(models.Model):
    id = models.AutoField(primary_key=True)
    subscription_type = models.CharField(max_length=300)
    subscription_price = models.IntegerField()

class AppConfigLookUpModel(models.Model):
    id = models.AutoField(primary_key=True)
    sender_payment_amount = models.IntegerField()
    receiver_payment_amount = models.IntegerField()