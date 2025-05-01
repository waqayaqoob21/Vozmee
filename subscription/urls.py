from django.urls import path
from subscription.views import *

urlpatterns = [
    path('CheckSubscriptionStatus', CheckSubscriptionStatus.as_view(), name='CheckSubscriptionStatus'),
    path('GetAllSubscriptions', GetAllSubscriptionsListAPIVIEW.as_view(), name='GetAllSubscriptions'),
    path('BuySubscription', UserSubscriptionAPIVIEW.as_view(), name='BuySubscription'),
    # path('UserPaymentDetail', UserPaymentDetailAPIVIEW.as_view(), name='UserPaymentDetail'),
    # path('UserBonus', UserBonusAPIVIEW.as_view(), name='UserBonus'),


]