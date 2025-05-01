from django.urls import path
from .views import *

urlpatterns = [
    path('Adminlogin/',AdminLoginAPIView.as_view(), name='adminlogin'), #req 1
    path('GetAllUsers/', ViewUserListAPIView.as_view(), name='getallusers'),#req6
    path('UserCount/', GetUserCountAPIView.as_view(), name='usercount'),# req 3
    path('UserActivation/', UserActivationView.as_view(), name='useractivation'), #req 10
    path('SearchUsers/', UserSearchAPIView.as_view(), name='searchusers'),# req 7
    path('GetSingleUser/', GetSingleUserAPIView.as_view(), name='getsingleuser'),#req 9
    path('TopEarningUsers/', TopEarningUsersAPIView.as_view(), name='topearningusers'),#req#4
    path('GetBalance/', GetActiveUsersBalanceAPIView.as_view(), name='getactiveusersbalance'),#req5
    path('GetCompanyEarnings/', CompanyEarningsAPIView.as_view(), name='companyearnings'), #req5.1
    path('AddRevenue/', AddRevenueAPIView.as_view(), name='add_revenue'),

    path('GetDateFilteredUserCount/', GetDateFilteredUserCountAPIView.as_view(), name='getmonthlyusercount'),#req 11




]













