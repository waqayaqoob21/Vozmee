from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from web_services.userController import *
from django.utils import timezone
from datetime import datetime, timedelta



user_obj = UserController()

            #========================= Admin login ===========================

class AdminLoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=AdminLoginSerializer,
        operation_description="Admin Login API",
        responses={
            200: "OK - Login successful",
            401: "Unauthorized - Invalid credentials"
        }
    )
    def post(self, request):
        result = user_obj.loginUser(request.data)
        return result

        # ==================================== View user list ========================================

class ViewUserListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('offset', openapi.IN_QUERY, description="Starting index of the items to return.",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Number of items to return per page.",
                              type=openapi.TYPE_INTEGER),

        ],
        operation_description='Get the list of all users.',
        responses={status.HTTP_200_OK: UserSerializer(many=True)},
    )

    def get(self, request):
        """
        Get the list of all users with pagination.

        Returns:
            - Paginated list of users.
        """
        result = user_obj.UserList(request)
        return result


            #======================== user count ======================================

class GetUserCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: UserCountSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def get(self, request):
        """
        Get user counts.

        Returns:
            - active_users: Number of active users.
            - non_active_users: Number of non-active users.
            - total_users: Total number of users.
            - total_admins: Total number of admin users.
        """
        result = user_obj.UserCount()
        return result
               # ====================== User activate/deactivate ===================

class UserActivationView(APIView):
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(
        request_body=UserActivationSerializer,
        responses={
            status.HTTP_200_OK: UserActivationResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "Invalid search query",
            status.HTTP_404_NOT_FOUND: 'User not found',
        },
    )

    def post(self, request):
        """
        Activate/Deactivate a user.

        user_id: ID of the user to be activated/deactivated.
        flag: True to activate, False to deactivate.
        """
        result = user_obj.UserActivation(request.data)
        return result

          # ============================== search user ===========================
class UserSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('search_query', openapi.IN_QUERY,
                              description="Search query for users by username, first name, last name, email, or phone number.",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('search_type', openapi.IN_QUERY,
                              description="Search type: name, email, phone_number, username",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('offset', openapi.IN_QUERY, description="Starting index of the items to return.",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Number of items to return per page.",
                              type=openapi.TYPE_INTEGER),

        ],
        responses={
            status.HTTP_200_OK: UserSearchResultSerializer(many=True, required=False),
            status.HTTP_400_BAD_REQUEST: "Invalid search query",
        },
    )
    def get(self, request):
        """
        Search users by username, first name, last name, email, or phone number.

        Returns:
            - List of users matching the search criteria.
        """
        search_query = request.query_params.get('search_query', '')
        search_type = request.query_params.get('search_type', '')
        limit = request.query_params.get('limit', None)
        offset = request.query_params.get('offset', None)

        result = user_obj.UserSearch(search_query, search_type,limit,offset)
        return result


                #======================= single user Details ====================
class GetSingleUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY,
                              description="User ID",
                              type=openapi.TYPE_INTEGER,
                              required= False),
        ],
        responses={
            status.HTTP_200_OK: SingleUserSerializer(),
            status.HTTP_404_NOT_FOUND: "User not found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        }
    )
    def get(self, request):
        """
        Get details of a single user by user ID.

        Returns:
            - Details of the requested user.
        """
        user_id = request.query_params.get('user_id')
        result = user_obj.SingleUserDetails(user_id)
        return result


    #========================top 10 highest earning users================
class TopEarningUsersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TopEarningUserSerializer(many=True,required= False),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def get(self, request):
        """
        Get top 10 earning users with their name, email, and earnings.

        Returns:
            - List of top 10 earning users with name, email, and earnings.
        """
        result = UserController.TopEarningUsers(request)
        return result

        # ======================Get Active Users Total Balnace ===================

class GetActiveUsersBalanceAPIView(APIView):
        permission_classes = [IsAuthenticated]

        @swagger_auto_schema(
                responses={
                    status.HTTP_200_OK: ActiveUsersBalanceSerializer(),
                    status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
                }
        )
        def get(self, request):

                response = user_obj.getbalance()
                return response


        # ======================Date Filtered User Count ===================

class GetDateFilteredUserCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'from_date',
                openapi.IN_QUERY,
                description="Start date for filtering (ISO 8601 date string, YYYY-MM-DD).",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                'to_date',
                openapi.IN_QUERY,
                description="End date for filtering (ISO 8601 date string, YYYY-MM-DD).",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={
            status.HTTP_200_OK: DateFilteredUserCountSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def get(self, request):
        """
        Query Parameters:
            - from_date (ISO 8601 date string): Start date for filtering.
            - to_date (ISO 8601 date string): End date for filtering.

        Returns:
            - active_users: Number of active users.
            - non_active_users: Number of non-active users.
            - total_users: Total number of users.
        """

        from_date_str = request.query_params.get('from_date')
        to_date_str = request.query_params.get('to_date')

        # Parse date strings into datetime objects
        from_date = datetime.fromisoformat(from_date_str) if from_date_str else None
        to_date = datetime.fromisoformat(to_date_str) if to_date_str else None
        result = user_obj.date_filtered_user_count(from_date, to_date)

        return result

       #======================Company Earnings ============================

class CompanyEarningsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: CompanyInfoSerializer(),
            status.HTTP_404_NOT_FOUND: "Company information not found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        }
    )
    def get(self, request):
        response = user_obj.get_company_earnings()
        return response

         #====================== Add Company Revenue ============================

class AddRevenueAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=AddRevenueSerializer,
        responses={
            status.HTTP_200_OK: CompanyInfoSerializer(),
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        }
    )
    def post(self, request):
        response = user_obj.add_revenue(request)
        return response