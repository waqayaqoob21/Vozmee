from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from user_management.userController import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

user_obj = UserController()

class SignUpUserAPIView(APIView):
    permission_classes = [AllowAny]
    # @swagger_auto_schema(
    #     request_body=NewUserSerializer,
    #     operation_description="Create a new user",
    # )
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['phone_number','username','email','password'],
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'referral_code': openapi.Schema(type=openapi.TYPE_STRING),

            },
        ),
        operation_description='Enter your comment'
    )
    def post(self, request):
        result = user_obj.signUpUser(request)
        return result

class UserLoginApiView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=LoginUserSerializer,
        operation_description="Login please",
    )
    def post(self, request):
        result = user_obj.loginUser(request.data)
        return result


# ==================================== Update User Data ========================================
class OtpForgetPasswordAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=ForgetPasswordSerializer,
        operation_description="Send OTP",

    )
    def post(self, request):
        result = user_obj.OtpForgetPassword(request.data)
        return result


class OtpVerifyOAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['otp','transaction_id'],
            properties={
                'otp': openapi.Schema(type=openapi.TYPE_STRING),
                'transaction_id': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        operation_description='Enter your comment'
    )
    def post(self, request):
        result = user_obj.verifyOtpForgetPassword(request)
        return result

class ResetPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        operation_description="Reset Password",
    )
    def post(self, request):
        result = user_obj.resetPassword(request)
        return result

# =========================== Verify OTP ========================
# =========================== Verify OTP ========================
class VerifyOtpAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['otp','transaction_id'],
            properties={
                'otp': openapi.Schema(type=openapi.TYPE_STRING),
                'transaction_id': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        operation_description='Enter your comment'
    )
    def post(self, request):
        result = user_obj.verifyOtp(request)
        return result

class ResendOtpAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        operation_description='Resend OTP'
    )
    def post(self, request):
        result = user_obj.resendOtp(request)
        return result

class UpdateProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'profile_picture': openapi.Schema(type=openapi.TYPE_FILE),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                'country': openapi.Schema(type=openapi.TYPE_STRING),
                'bio': openapi.Schema(type=openapi.TYPE_STRING),
                'gender': openapi.Schema(type=openapi.TYPE_STRING),
                'age': openapi.Schema(type=openapi.TYPE_STRING),

            },
        ),
        operation_description='Enter your comment'
    )
    def post(self, request):
        result = user_obj.updateProfile(request)
        return result
class GetUserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        result = user_obj.getUserProfile(request)
        return result
