from django.http import JsonResponse
from subscription.serializer import *
from subscription.models import *
from loopService.statuses import *
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import random
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import boto3  # pip install boto3
import os,shutil
import random
import string
from django.db import connection
class SubscriptionController:

    @staticmethod
    def checkSubscriptionStatus(request):
        try:
            user_id = request.user.id
            is_subscription = UserPaymentDetail.objects.filter(user_id = user_id, is_payment = True).first()
            if is_subscription is None:
                return JsonResponse({'message': 'Blocked', 'success': False, 'data': [], 'status': 401},
                                    status=200)
            else:
                return JsonResponse(
                    {'message': 'Continue', 'success': True, 'data': [], 'status': 200},
                    status=200)

        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Subscription status could not check', 'success': False, 'data': [], 'status': 500},
                                status=500)
    @staticmethod
    def getAllSubscriptions(request):
        try:
            subcription_list = SubscriptionLookUpModel.objects.all()
            serializer = SubscriptionTypeSerializer(subcription_list, many=True)
            return JsonResponse({'message': 'Subscription types fetched successfully','success': True, 'data': serializer.data,'status':200},
                                    status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Subscription types could not fetch','success': False, 'data': [], 'status':500}, status=500)

    @staticmethod
    def userSubscription(request):
        try:
            user_id = request.user.id
            sub_id = request.data['subscription_id']
            subscription = UserSubscription.objects.filter(user_id = user_id).first()
            subscription_type = SubscriptionLookUpModel.objects.filter(id=sub_id).first()

            if subscription is None:
                subscriptionModel = UserSubscription()
                subscriptionModel.user_id = user_id
                subscriptionModel.subscription_type_id = sub_id
                subscriptionModel.subscription_amount = subscription_type.subscription_price
                subscriptionModel.updated_at = None
                subscriptionModel.save()
                if UserSubscription.objects.filter(user_id = user_id):
                    userPayment = UserPaymentDetail()
                    userPayment.user_id = user_id
                    userPayment.is_payment  = True
                    end_time = datetime.now()
                    if sub_id == '1':
                        end_time += relativedelta(months=3)
                    elif sub_id == '2':
                        end_time += relativedelta(months=6)
                    else:
                        end_time += relativedelta(years=1)
                    userPayment.expiry_date = end_time
                    userPayment.amount = subscription_type.subscription_price
                    userPayment.referral_code = random.randint(1000,9999)
                    userPayment.save()
                userPyamentDetail = UserPaymentDetail.objects.filter(user_id = user_id).first()
                serializer = UserPaymentDetailSerializer(userPyamentDetail)
                return JsonResponse({'message': 'Subscription successful','success': True, 'data': serializer.data,'status':200},
                                    status=200)
            else:
                if subscription.subscription_type_id != sub_id:
                    subscriptionHistory = UserSubscriptionHistory()
                    subscriptionHistory.user_id = user_id
                    subscriptionHistory.subscription_type_id = subscription_type.id
                    subscriptionHistory.subscription_amount = subscription.subscription_amount
                    subscriptionHistory.updated_at = subscription.updated_at
                    subscriptionHistory.user_subscription_id = subscription.id
                    subscriptionHistory.save()

                subscription.user_id = user_id
                subscription.subscription_type_id = subscription_type.id
                subscription.subscription_amount = subscription_type.subscription_price
                subscription.updated_at = datetime.now()
                subscription.save()
                if UserSubscription.objects.filter(user_id = user_id):
                    getUserPaymentDetail = UserPaymentDetail.objects.filter(user_id = user_id).first()
                    if getUserPaymentDetail is not None:
                        userPaymentHistory = UserPaymentDetailHistory()
                        userPaymentHistory.user_id = getUserPaymentDetail.user_id
                        userPaymentHistory.is_payment = True
                        userPaymentHistory.amount = getUserPaymentDetail.amount
                        userPaymentHistory.payment_date = getUserPaymentDetail.payment_date
                        userPaymentHistory.expiry_date = getUserPaymentDetail.expiry_date
                        userPaymentHistory.referral_code = getUserPaymentDetail.referral_code
                        userPaymentHistory.user_payment_id = getUserPaymentDetail.id
                        userPaymentHistory.save()

                    getUserPaymentDetail.user_id = user_id
                    getUserPaymentDetail.is_payment = True
                    end_time = datetime.now()
                    if sub_id == '1':
                        end_time += relativedelta(months=3)
                    elif sub_id == '2':
                        end_time += relativedelta(months=6)
                    else:
                        end_time += relativedelta(years=1)
                    getUserPaymentDetail.expiry_date = end_time
                    getUserPaymentDetail.amount = subscription_type.subscription_price
                    getUserPaymentDetail.referral_code = random.randint(1000,9999)
                    getUserPaymentDetail.save()
                userPyamentDetail = UserPaymentDetail.objects.filter(user_id = user_id).first()
                serializer = UserPaymentDetailSerializer(userPyamentDetail)
                return JsonResponse({'message': 'User subscription updated successfully','success': True, 'data': serializer.data,'status':200},
                                    status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Subscription failed','success': False, 'data': [], 'status':500}, status=500)

    @staticmethod
    def userPaymentDetail(request):
        try:
            pass
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Videos could not fetch','success': False, 'data': [], 'status':500}, status=500)

    @staticmethod
    def userBonus(request):
        try:
            pass
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Videos could not fetch','success': False, 'data': [], 'status':500}, status=500)