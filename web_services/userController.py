from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import *
from user_management.models import *
from django.db.models import Q
from subscription.models import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum
from .models import CompanyInfo



class UserController:
    @staticmethod
    def loginUser(data):
        try:
            serializer = AdminLoginSerializer(data=data)
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']

                user = None
                if '@' in username:
                    user = User.objects.filter(Q(email=username) | Q(username=username)).first()
                else:
                    user = authenticate(username=username, password=password)



                if user   and  user.is_active and user.is_superuser and user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token
                    access_token['name'] = user.username

                    admin_details = {
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'username': user.username,
                        'email': user.email,
                    }

                    response_data = {
                        'token': str(access_token),
                        'admin_details': admin_details
                    }
                    return JsonResponse({'message': "Login Successfully", 'success': True, 'data': response_data, 'status': 200}, status=200)

                else:
                    return JsonResponse({'message': 'Invalid credentials', 'success': False, 'data': {},'status':status.HTTP_401_UNAUTHORIZED },status =401)
            else:
                return JsonResponse({'message': 'Invalid input data', 'success': False, 'data': {}, 'status':status.HTTP_400_BAD_REQUEST},status =400)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "Login failed", 'success': False, 'data': {}, 'status': 500}, status=500)
    @staticmethod
    def UserList(request):

        try:
            limit = request.query_params.get('limit')
            offset = request.query_params.get('offset')

            users = User.objects.all()[int(offset):int(offset) + int(limit)]
            serializer = UserSerializer(users, many=True)
            if users:
                return JsonResponse({'message': 'Users fetched successfully','success': True,
                                     'data': serializer.data, 'status': 200},status=200)
            else:
                return JsonResponse({'message': 'No user found', 'success': False, 'data': [], 'status': 401},
                                    status=401)
        except Exception as e:
            print(e)
            return JsonResponse(
                {'message': 'User data could not be fetched', 'success': False, 'data': [], 'status': 500},
                                      status=500)




    @staticmethod
    def UserCount():
        try:
            active_users = User.objects.filter(is_active=True).count()
            non_active_users = User.objects.filter(is_active=False).count()
            total_users = User.objects.exclude(is_superuser=True).count()
            total_admins = User.objects.filter(is_superuser=True).count()

            data = {
                'active_users': active_users,
                'non_active_users': non_active_users,
                'total_users': total_users,
                'total_admins': total_admins,
            }

            if active_users == 0:
                data['active_users'] = 0
            if non_active_users == 0:
                data['non_active_users'] = 0

            serializer = UserCountSerializer(data=data)

            if serializer.is_valid():
                return JsonResponse(
                    {'message': 'User count fetched successfully', 'success': True, 'data': serializer.validated_data,
                     'status': 200}, status=200)
            else:
                return JsonResponse({'message': 'Serialization error', 'success': False, 'data': [],
                                     'status': status.HTTP_500_INTERNAL_SERVER_ERROR},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            print(e)
            return JsonResponse({'message': 'An error occurred', 'success': False, 'data': [],
                                 'status': status.HTTP_500_INTERNAL_SERVER_ERROR},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def UserActivation(data):
        try:
            serializer = UserActivationSerializer(data=data)
            if serializer.is_valid():
                user_id = serializer.validated_data['user_id']
                flag = serializer.validated_data['flag']
                try:
                    user = User.objects.get(id=user_id)
                    user.is_active = flag
                    user.save()
                    action = "activated" if flag else "deactivated"
                    response_data = {}

                    return JsonResponse({'message': f'User {action} successfully','success': True,'data':[] ,
                                         'status': status.HTTP_200_OK},status=200)
                except User.DoesNotExist:

                    return JsonResponse({'message': 'User not found','success': False,'data':[] ,
                                   'status': status.HTTP_404_NOT_FOUND},status=404)

            else:
                return JsonResponse({'message': 'Invalid request data','success': False,'data':[] ,
                                    'status':status.HTTP_400_BAD_REQUEST }, status=s400)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'An error occurred','success': False,'data':[] ,
                                'status':status.HTTP_500_INTERNAL_SERVER_ERROR }, status= 500)

    @staticmethod
    def UserSearch(search_query, search_type, limit, offset):
        try:
            users = User.objects.none()

            if search_type == 'name':
                users = User.objects.filter(first_name__icontains=search_query)
            elif search_type == 'email':
                users = User.objects.filter(email__icontains=search_query)
            elif search_type == 'phone_number':
                users = User.objects.filter(phone_number__icontains=search_query)
            elif search_type == 'username':
                users = User.objects.filter(username__icontains=search_query)

            if limit is not None and offset is not None:
                  users = users[int(offset):int(offset) + int(limit)]

            if users.exists():
                serializer = UserSearchResultSerializer(users, many=True)
                return JsonResponse({'message': 'Users fetched successfully', 'success': True, 'data': serializer.data,
                                     'status': status.HTTP_200_OK}, status=200)
            else:
                return JsonResponse({'message': 'User not found', 'success': False, 'data': [],
                                     'status': status.HTTP_404_NOT_FOUND}, status=404)

        except Exception as e:
            print(e)
            return JsonResponse({'message': 'An error occurred', 'success': False, 'data': [],
                                 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=500)

    @staticmethod
    def SingleUserDetails(user_id):

        try:
            try:
                user = User.objects.get(id=user_id)
                serializer = SingleUserSerializer(user)
                return JsonResponse(
                    {'message': 'User data fetched successfully', 'success': True, 'data': serializer.data,
                     'status': 200}, status=200)

            except User.DoesNotExist:
                return JsonResponse({'message': 'User not found', 'success': False, 'data': [],
                                     'status': status.HTTP_404_NOT_FOUND}, status=404)

        except Exception as e:
            print(e)
            return JsonResponse({'message': 'An error occurred', 'success': False, 'data': [],
                                 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}, status=500)

    @staticmethod
    def TopEarningUsers(request):

        try:
            top_earning_users = UserBonus.objects.order_by('-balance')[:10]
            serializer = TopEarningUserSerializer(top_earning_users, many=True)

            return JsonResponse(
                {'message': 'Top earning users fetched successfully', 'success': True, 'data': serializer.data,
                 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'An error occurred', 'success': False, 'data': [],
                                 'status': status.HTTP_500_INTERNAL_SERVER_ERROR},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def getbalance():
        try:
            # Get the list of active user IDs
            active_user_ids = User.objects.filter(is_active=True).values_list('id', flat=True)

            # Calculate the total balance of active users
            total_active_users_balance = \
                UserBonus.objects.filter(user_id__in=active_user_ids).aggregate(total_balance=Sum('balance'))[
                    'total_balance']

            if total_active_users_balance is None:
                total_active_users_balance = Decimal('0.00')

            response_data = {
                'total_active_users_balance': total_active_users_balance,
            }

            return JsonResponse(
                {'message': 'Total balance of active users fetched successfully', 'success': True,
                 'data': response_data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return JsonResponse({'message': 'An error occurred', 'success': False, 'data': [],
                                 'status': status.HTTP_500_INTERNAL_SERVER_ERROR},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @staticmethod
    def date_filtered_user_count(from_date=None, to_date=None):
        try:

            if to_date:
                to_date_end = to_date + timedelta(days=1)
            else:
                to_date_end = None

            active_users = User.objects.filter(is_active=True, is_superuser=False)
            non_active_users = User.objects.filter(is_active=False, is_superuser=False)
            total_users = User.objects.exclude(is_superuser=True)

            if from_date:
                active_users = active_users.filter(date_joined__gte=from_date)
                non_active_users = non_active_users.filter(date_joined__gte=from_date)
                total_users = total_users.filter(date_joined__gte=from_date)

            if to_date_end:
                active_users = active_users.filter(date_joined__lt=to_date_end)
                non_active_users = non_active_users.filter(date_joined__lt=to_date_end)
                total_users = total_users.filter(date_joined__lt=to_date_end)


            active_user_count = active_users.count()
            non_active_user_count = non_active_users.count()
            total_user_count = total_users.count()

            data = {
                'active_users': active_user_count,
                'non_active_users': non_active_user_count,
                'total_users': total_user_count,
            }

            return JsonResponse(
                {'message': 'User count fetched successfully', 'success': True, 'data': data, 'status': 200}
            )

        except Exception as e:
            print(e)
            return JsonResponse(
                {'message': 'An error occurred', 'success': False, 'data': [],
                 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}
            )

    @staticmethod
    def get_company_earnings():
        try:

            company_info_records = CompanyInfo.objects.all()


            monthly_revenue = []
            for company_info in company_info_records:
                month = company_info.month_name.capitalize()
                year = company_info.year_name
                revenue = float(company_info.total_revenue)


                monthly_revenue.append({
                    'month': month,
                    'year': year,
                    'revenue': str(revenue)
                })

            data = {
                'message': 'Company Earnings Fetched Successfully',
                'success': True,
                'data': monthly_revenue
            }
            return JsonResponse(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)  # Log the error for debugging purposes
            return JsonResponse({
                'message': 'An error occurred',
                'success': False,
                'data': [],
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def add_revenue(request):
        try:
            # Validate request data using AddRevenueSerializer
            serializer = AddRevenueSerializer(data=request.data)
            if serializer.is_valid():
                # Get validated input parameters from serializer
                revenue = serializer.validated_data.get('revenue')
                month_name = serializer.validated_data.get('month_name').capitalize()
                year_name = serializer.validated_data.get('year_name')

                # Query the CompanyInfo model based on month and year
                company_info = CompanyInfo.objects.filter(month_name=month_name, year_name=year_name).first()

                if company_info:

                    company_info.total_revenue += revenue
                    company_info.save()
                else:

                    CompanyInfo.objects.create(
                        month_name=month_name,
                        year_name=year_name,
                        total_revenue=revenue,
                        name='Vozee',
                        description='Company description'
                    )

                # Serialize the updated or created CompanyInfo object
                serializer = CompanyInfoSerializer(company_info)

                # Prepare the success response data
                data = {
                    'message': 'Revenue added successfully',
                    'success': True,
                    'data': serializer.data
                }

                return JsonResponse(data, status=status.HTTP_200_OK)


            return JsonResponse({'message': 'Bad Request', 'success': False, 'data': serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)


            data = {
                'message': 'Internal Server Error',
                'success': False,
                'data': []
            }

            return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)