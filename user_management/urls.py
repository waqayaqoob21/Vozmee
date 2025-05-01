
from django.urls import path
from user_management.views import *

urlpatterns = [
    path('Register', SignUpUserAPIView.as_view(), name='Register'),
    path('SignIn', UserLoginApiView.as_view(), name='SignIn'),
    path('VerifyOtpForLogin', VerifyOtpAPIView.as_view(), name='VerifyOtpForLogin'),
    path('ForgetPassword', OtpForgetPasswordAPIView.as_view(), name='ForgetPassword'),
    path('ResetPassword', ResetPasswordAPIView.as_view(), name='ResetPassword'),
    path('UpdateProfile', UpdateProfileAPIView.as_view(), name='UpdateProfile'),
    path('OtpVerifyForForgetPassword', OtpVerifyOAPIView.as_view(), name='VerifyOtpForPasswordReset'),
    path('ResendOtp', ResendOtpAPIView.as_view(), name='ResendOtp'),
    path('GetProfile', GetUserProfileAPIView.as_view(), name='GetProfile'),

]