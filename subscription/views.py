from drf_yasg import openapi
from rest_framework.views import APIView
from subscription.subController import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


ctrlObj = SubscriptionController()

class CheckSubscriptionStatus(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        result = ctrlObj.checkSubscriptionStatus(request)
        return result
class GetAllSubscriptionsListAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = ctrlObj.getAllSubscriptions(request.data)
        return result

class UserSubscriptionAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['subscription_id'],
            properties={
                'subscription_id': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        operation_description='Enter your comment'
    )
    def post(self, request):
        result = ctrlObj.userSubscription(request)
        return result
class UserPaymentDetailAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['is_payment','amount'],
            properties={
                'video_id': openapi.Schema(type=openapi.TYPE_STRING),

            },
        ),
        operation_description='Enter your comment'
    )
    def post(self, request):
        result = ctrlObj.userPaymentDetail(request.data)
        return result

class UserBonusAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['video_id'],
            properties={
                'video_id': openapi.Schema(type=openapi.TYPE_STRING),

            },
        ),
        operation_description='Enter your comment'
    )
    def post(self, request):
        result = ctrlObj.userBonus(request.data)
        return result