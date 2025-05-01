from django.http import JsonResponse
from user_management.serializer import *
from loopService.statuses import *
from subscription.models import *
from subscription.serializer import *
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import random
from django.contrib.auth import authenticate, login
from rest_framework.fields import CharField, IntegerField, DateTimeField, EmailField
from django.core.files.storage import FileSystemStorage
import boto3  # pip install boto3
import os,shutil
import string
from django.db import connection


class UserController:
    @staticmethod
    def signUpUser(request):
        try:
            userModel = User()
            serializer = NewUserSerializer(data=request.data)
            if serializer.is_valid():
                request = request.data
                email = User.objects.filter(email=request['email']).first()
                username = User.objects.filter(username=request['username']).first()
                if email is None and username is None:
                    userModel.first_name = ""
                    userModel.last_name = ""
                    userModel.username = request['username']
                    userModel.email = request['email']
                    # userModel.password = request['password']
                    encryptedpassword = make_password(request['password'])
                    userModel.password = encryptedpassword
                    userModel.is_superuser = 'True'
                    userModel.last_login = date.today()
                    userModel.is_active = 'True'
                    userModel.is_staff = 'True'
                    userModel.phone_number = request['phone_number']
                    if request['referral_code'] != '' and request['referral_code'] != 'string':
                        referral_code = request['referral_code']
                        userPaymentModel = UserPaymentDetail.objects.filter(referral_code = referral_code).first()
                        if userPaymentModel is not None:
                            userBonusAmount = AppConfigLookUpModel.objects.first()
                            user_id = userPaymentModel.user_id
                            userBonus = UserBonus.objects.filter(user_id = user_id).first()
                            inital_balance = 0
                            if userBonus is None:
                                userBonusModel = UserBonus()
                                userBonusModel.user_id = user_id
                                if userBonusModel.balance is None:
                                    userBonusModel.balance = inital_balance + userBonusAmount.sender_payment_amount
                                userBonusModel.save()
                                userModel.save()
                                getReceiver = User.objects.filter(email=request['email']).first()
                                if getReceiver is not None:
                                    userReceiverBonusModel = UserBonus()
                                    userReceiverBonusModel.user_id = getReceiver.id
                                    userReceiverBonusModel.balance = userBonusAmount.receiver_payment_amount
                                    userReceiverBonusModel.save()
                            else:
                                if userBonus is not None:
                                    userBonusHistory = UserBonusHistory()
                                    userBonusHistory.user_id = userBonus.user_id
                                    userBonusHistory.balance = userBonus.balance
                                    userBonusHistory.user_bonus_id = userBonus.id
                                    userBonusHistory.save()
                                userBonus.user_id = user_id
                                userBonus.balance = userBonus.balance + userBonusAmount.sender_payment_amount
                                userBonus.updated_at = datetime.now()
                                userBonus.save()
                                userModel.save()
                                getReceiver = User.objects.filter(email = request['email']).first()
                                if getReceiver is not None:
                                    userReceiverBonusModel = UserBonus()
                                    userReceiverBonusModel.user_id = getReceiver.id
                                    userReceiverBonusModel.balance = userBonusAmount.receiver_payment_amount
                                    userReceiverBonusModel.save()
                            return JsonResponse(
                                {'message': 'User added successfully!', 'success': True, 'data': [], 'status': 200},
                                status=200)
                        else:
                            return JsonResponse({'message': "Invalid referral code", 'success': False, 'data': [], 'status': 403},
                                               status=403)
                    userModel.save()
                    return JsonResponse(
                        {'message': 'User added successfully!', 'success': True, 'data': [], 'status': 200}, status=200)
                else:
                    msg=""
                    if email:
                        msg = "A user with that email already exists."
                    if username:
                        msg = "A user with that username already exists."
                    if username and email:
                        msg = "A user with that email already exists \n A user with that username already exists."
                    return JsonResponse(
                            {'message': msg, 'success': False, 'data': [],
                             'status': 403}, status=403)
            else:
                msg = ""
                if 'phone_number' in serializer.errors.keys():
                    msg = 'Enter valid phone number'
                if 'email' in serializer.errors.keys():
                    msg = "Enter a valid email address"
                if 'email' in serializer.errors.keys() and 'phone_number' in serializer.errors.keys():
                    msg = "Enter valid phone number \n Enter valid email address"
                return JsonResponse({'message': msg, 'success': False, 'data': [], 'status': 403}, status=403)

        except Exception as e:
            print(e)
            return JsonResponse({'message': statusList.error_failed, 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def loginUser(request):
        try:
            serializer = LoginUserSerializer(data=request)
            if serializer.is_valid():
                user = {}
                if request['username'] != '':
                    username = request['username']
                    password = request['password']
                    if '@' in username:
                        if User.objects.filter(email=username).exists():
                            user = User.objects.get(email=username)
                            if user.check_password(raw_password=password):
                                user = user
                    else:
                        user = authenticate(request, username=username, password=password)
                if user:
                    otpObj = otpLogin.objects.filter(user_id=user.id).first()
                    if otpObj is None:
                        otpModel = otpLogin()
                        otp = random.randint(1000, 9999)
                        tranaction_id = random.randint(10000000, 99999999)
                        otpModel.otp = otp
                        otpModel.transaction_id = tranaction_id
                        otpModel.user_id = user.id
                        otpModel.save()
                        user_data = {'otp': otp, 'transaction_id': tranaction_id, 'user_id': user.id}
                        return JsonResponse(
                            {'message': "OTP sent!", 'success': True, 'data': user_data, 'status': 200}, status=200)
                    else:
                        otpObj.otp = random.randint(1000, 9999)
                        otpObj.save()
                        user_data = {'otp': otpObj.otp, 'transaction_id': otpObj.transaction_id,
                                     'user_id': otpObj.user_id}
                        return JsonResponse(
                            {'message': "OTP sent!", 'success': True, 'data': user_data, 'status': 200}, status=200)
                else:
                    return JsonResponse(
                        {'message': "Invalid username or password", 'success': False, 'data': {}, 'status': 401},
                        status=403)
            else:
                return JsonResponse(
                    {'message': "Invalid username or password", 'success': False, 'data': {}, 'status': 401},
                    status=401)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "Login failed", 'success': False, 'data': {}, 'status': 500},
                                status=500)

    # ============================ Verify OTP for Login =================================
    # ============================ Verify OTP for Login =================================
    @staticmethod
    def verifyOtp(request):
        try:

            otp = request.data['otp']
            transaction_id = request.data['transaction_id']
            serializer = LoginOtpSerializer(data=request.data)
            if serializer.is_valid():
                user_data = otpLogin.objects.filter(otp=otp, transaction_id=transaction_id).first()
                if user_data is not None:
                    # Token Generator
                    def get_tokens_for_user(user):
                        refresh = RefreshToken.for_user(user)
                        access_token = refresh.access_token
                        access_token['name'] = user.username
                        return access_token
                        # return {
                        #     'refresh': str(refresh),
                        #     'access': str(refresh.access_token),
                        # }

                    user = User.objects.get(id=user_data.user_id)
                    if user is not None:
                        token = get_tokens_for_user(user)
                        user_data = {'id': user.id, 'username': user.username,
                                     'email': user.email, 'is_superuser': user.is_superuser,
                                     'phone_number': user.phone_number
                                     }
                        return JsonResponse(
                            {'message': "Login successfully", 'success': True, 'data': user_data, 'token': str(token),
                             'status': 200}, status=200)
                    else:
                        return JsonResponse(
                            {'message': 'No user found. Login Failed!', 'success': False, 'data': {}, 'status': 403},
                            status=403)
                else:
                    return JsonResponse(
                        {'message': "Invalid OTP or Transaction ID!", 'success': False, 'data': {}, 'status': 403},
                        status=403)
            else:
                return JsonResponse(
                    {'message': 'Enter valid OTP or Transaction ID please!', 'success': False, 'data': {},
                     'status': 401}, status=401)

        except Exception as e:
            print(e)
            return JsonResponse({'message': "Login failed", 'success': False, 'data': {}, 'status': 500}, status=500)

    # ===================================Updation APIs====================================
    @staticmethod
    def OtpForgetPassword(request):
        try:
            serializer = ForgetPasswordSerializer(data=request)
            if serializer.is_valid():
                userObj = User.objects.filter(email=request['email']).first()
                otpObj = otpLogin.objects.filter(user_id=userObj.id).first()
                if otpObj is None:
                    otpModel = otpLogin()
                    otp = random.randint(1000, 9999)
                    tranaction_id = random.randint(10000000, 99999999)
                    otpModel.otp = otp
                    otpModel.transaction_id = tranaction_id
                    otpModel.user_id = otpObj.user_id
                    otpModel.save()
                    user_data = {'otp': otp, 'transaction_id': tranaction_id, 'user_id': otpObj.user_id}
                    return JsonResponse(
                        {'message': "OTP sent!", 'success': True, 'data': user_data, 'status': 200}, status=200)
                else:
                    otpObj.otp = random.randint(1000, 9999)
                    otpObj.save()
                    user_data = {'otp': otpObj.otp, 'transaction_id': otpObj.transaction_id, 'user_id': otpObj.user_id}
                    return JsonResponse(
                        {'message': "OTP sent!", 'success': True, 'data': user_data, 'status': 200}, status=200)
            else:
                return JsonResponse(
                    {'message': "Invalid username or password", 'success': False, 'data': {}, 'status': 401},
                    status=401)
        except Exception as e:
            print(e)
            return JsonResponse({'message': statusList.error_not_found, 'success': False, 'data': {}, 'status': 500},
                                status=500)

    @staticmethod
    def resetPassword(request):
        try:
            id = request.user.id  # Fetching user id from JWT Token
            userModel = User.objects.filter(id=id)
            serializer = UserSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                if userModel is not None:
                    encryptedpassword = make_password(request.data['password'])
                    password = encryptedpassword
                    userModel.update(password=password)
                    return JsonResponse(
                        {'message': "Password reset successfully!", 'success': True, 'data': [], 'status': 200},
                        status=200)
            else:
                return JsonResponse(
                    {'message': 'Enter valid password please!', 'success': False, 'data': [], 'status': 401},
                    status=401)

        except Exception as e:
            print(e)
            return JsonResponse({'message': statusList.error_not_found, 'success': False, 'data': [], 'status': 500},
                                status=500)

    # =================================== Verify OTP for Forget Password=======================================
    # =================================== Verify OTP for Forget Password=======================================
    @staticmethod
    def verifyOtpForgetPassword(request):
        try:
            otp = request.data['otp']
            transaction_id = request.data['transaction_id']
            serializer = LoginOtpSerializer(data=request.data)
            if serializer.is_valid():
                user_data = otpLogin.objects.filter(otp=otp, transaction_id=transaction_id).first()
                user = User.objects.get(id=user_data.user_id)

                if user_data is not None and user is not None:
                    # user_data = {'id': user.id, 'username': user.username,
                    #              'email': user.email, 'is_superuser': user.is_superuser,
                    #              'phone_number': user.phone_number
                    #              }
                    return JsonResponse(
                        {'message': "Authorized user! please reset your password now.", 'success': True, 'data': [],
                         'status': 200},
                        status=200)
                else:
                    return JsonResponse(
                        {'message': "Invalid OTP or Transaction ID!", 'success': False, 'data': [], 'status': 403},
                        status=403)
            else:
                return JsonResponse(
                    {'message': "Invalid OTP or Transaction ID!", 'success': False, 'data': [], 'status': 401},
                    status=401)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "Login failed", 'success': False, 'data': [], 'status': 500}, status=500)


    @staticmethod
    def resendOtp(request):
        try:
            user = {}
            if request.data['username'] != '':
                username = request.data['username']
                if '@' in username:
                    if User.objects.filter(email=username).exists():
                        user = User.objects.get(email=username)
                else:
                    if User.objects.filter(username=username).exists():
                        user = User.objects.get(username=username)
            if user:
                otpObj = otpLogin.objects.filter(user_id=user.id).first()
                if otpObj is not None:
                    otp = random.randint(1000, 9999)
                    tranaction_id = random.randint(10000000, 99999999)
                    otpObj.otp = otp
                    otpObj.transaction_id = tranaction_id
                    otpObj.user_id = user.id
                    otpObj.save()
                    user_data = {'otp': otpObj.otp, 'transaction_id': otpObj.transaction_id,'user_id': otpObj.user_id}
                    return JsonResponse(
                            {'message': "OTP sent!", 'success': True, 'data': user_data, 'status': 200}, status=200)
                else:
                    return JsonResponse(
                            {'message': "Invalid username or email", 'success': False, 'data': {}, 'status': 401},
                            status=403)
            else:
                return JsonResponse(
                        {'message': "Invalid username or email", 'success': False, 'data': {}, 'status': 401},
                        status=403)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "OTP authentication failed", 'success': False, 'data': {}, 'status': 500}, status=500)


    @staticmethod
    def updateProfile(request):
        try:
            if request.data is not None and request.data != {}:
                msg = ""
                userModel = User.objects.filter(id=request.user.id).first()
                if 'first_name' in request.data:
                    userModel.first_name = request.data['first_name']
                if 'last_name' in request.data:
                    userModel.last_name = request.data['last_name']
                if 'phone_number' in request.data:
                    userModel.phone_number = request.data['phone_number']
                if 'phone_number' in request.data or 'last_name' in request.data or 'first_name' in request.data:
                    userModel.save()
                profileModel = Profile.objects.filter(user_id=request.user.id).first()
                if profileModel is None:
                    userProfile = Profile()
                    newFileNamePath=""
                    if 'profile_picture' in request.data:
                        fs = FileSystemStorage()
                        file = request.data['profile_picture']
                        target_path = 'myPictures/'
                        filenamepath = fs.save(target_path + file.name, file)
                        filename = file.name
                        # local_file_url = fs.url(filename)
                        type = os.path.splitext(filename)
                        file_type =type[1]
                        # local_file_url = fs.url(filename)
                        if file_type == '.jpeg' or file_type == '.jpg' or file_type == '.png':
                            name = ''.join(random.choice(string.ascii_letters) for i in range(10))
                            newFileName = name+file_type
                            newFileNamePath = target_path + newFileName
                            os.rename(filenamepath, newFileNamePath)

                            print(newFileNamePath);
                            # Let's use Amazon S3
                            file_url = 'https://vozmee-assets.s3.amazonaws.com/' + newFileName
                            s3 = boto3.resource("s3")
                            bucket = s3.Bucket("vozmee-assets")
                            # Print out bucket names
                            file_extension = file_type.split('.')[1]
                            bucket.upload_file(Key=newFileName, Filename=newFileNamePath,
                                               ExtraArgs={'ContentType': "image/"+file_extension})
                            profileModel.profile_picture = file_url
                        else:
                            msg = "Please upload valid image"
                    if 'country' in request.data:
                        userProfile.country = request.data['country']
                    if 'bio' in request.data:
                        userProfile.bio = request.data['bio']
                    if 'gender' in request.data:
                        userProfile.gender = request.data['gender']
                    if 'age' in request.data:
                        userProfile.age = request.data['age']
                    userProfile.referral_code = random.randint(100000, 999999)
                    userProfile.user_id = request.user.id
                    userProfile.save()
                    if os.path.isfile(newFileNamePath):
                        os.remove(newFileNamePath)
                else:
                    newFileNamePath=""
                    if 'profile_picture' in request.data:
                        fs = FileSystemStorage()
                        file = request.data['profile_picture']
                        target_path = 'myPictures/'
                        filenamepath = fs.save(target_path + file.name, file)
                        filename = file.name
                        # file_type = filename.split('.')[1]
                        type = os.path.splitext(filename)
                        file_type =type[1]
                        # local_file_url = fs.url(filename)
                        if file_type == '.jpeg' or file_type == '.jpg' or file_type == '.png':
                            name = ''.join(random.choice(string.ascii_letters) for i in range(10))
                            newFileName = name+file_type
                            newFileNamePath = target_path + newFileName
                            os.rename(filenamepath, newFileNamePath)

                            print(newFileNamePath);
                            # Let's use Amazon S3
                            file_url = 'https://vozmee-assets.s3.amazonaws.com/' + newFileName
                            s3 = boto3.resource("s3")
                            bucket = s3.Bucket("vozmee-assets")
                            # Print out bucket names
                            file_extension = file_type.split('.')[1]
                            bucket.upload_file(Key=newFileName, Filename=newFileNamePath,
                                               ExtraArgs={'ContentType': "image/"+file_extension})
                            profileModel.profile_picture = file_url
                        else:
                            msg = "Please upload valid image"
                    if 'country' in request.data:
                        profileModel.country = request.data['country']
                    if 'bio' in request.data:
                        profileModel.bio = request.data['bio']
                    if 'gender' in request.data:
                        profileModel.gender = request.data['gender']
                    if 'age' in request.data:
                        profileModel.age = request.data['age']
                    profileModel.user_id = request.user.id
                    profileModel.save()
                    if os.path.isfile(newFileNamePath):
                        os.remove(newFileNamePath)
                if msg == "":
                    return JsonResponse(
                            {'message': "Profile updated successfully!", 'success': True, 'data': [], 'status': 200},
                            status=200)
                else:
                    return JsonResponse(
                            {'message': "Profile updated successfully, but could not upload image due to invalid image type.", 'success': True, 'data': [], 'status': 200},
                            status=200)

            else:
                return JsonResponse(
                    {'message': 'No information is given to update user profile', 'success': True, 'data': [], 'status': 200}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'User profile could not update', 'success': False, 'data': [], 'status': 500},
                                status=500)
    @staticmethod
    def getUserProfile(request):
        try:
            id = request.user.id  # Fetching user id from JWT Token
            user_profile = []
            cm_cursor = connection.cursor()
            cm_query = "SELECT u.id,u.username,u.email,COALESCE(u.first_name,'') As first_name ,COALESCE(u.last_name,'') As last_name,u.phone_number,COALESCE(up.profile_picture,'') As profile_picture,COALESCE(up.bio,'') As bio, " \
                           "COALESCE(up.country,'') As country,COALESCE(up.gender,'') As gender,COALESCE(up.age,'') As age,COALESCE(up.referral_code,'') As referral_code "\
                           "FROM user_management_user u " \
                           "FULL JOIN user_management_profile up ON u.id = up.user_id WHERE u.id = " +str(id)
            cm_cursor.execute(cm_query)
            cm_col_names = [col[0] for col in cm_cursor.description]
            for row in cm_cursor.fetchall():
                row_dict = dict(zip(cm_col_names, row))
                user_profile.append(row_dict)
            return JsonResponse(
                {'message': 'User data fetched successfully', 'success': True, 'data': user_profile, 'status': 200},
                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "Could not get user profile", 'success': False, 'data': [], 'status': 500},
                                status=500)
