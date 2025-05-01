from django.http import JsonResponse
from videos.serializer import *
from user_management.models import *
from loopService.statuses import *
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import random
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import boto3  # pip install boto3
import os, shutil
import random
import string
from django.db import connection
from moviepy.editor import *




class VideoController:

    @staticmethod
    def uploadVideo(request):
        try:
            videoModel = Videos()
            fs = FileSystemStorage()
            file = request.data['file']
            music_name = ""
            music_id = ""
            if 'music_id' in request.data:
                music_id = request.data['music_id']
                music = Music.objects.filter(music_id=music_id).first()
                if music is not None:
                    music_name = music.name
                else:
                    music_name = ""
            if not os.path.isdir('myVideos'):
                os.mkdir('myVideos')
            target_path = 'myVideos/'
            filenamepath = fs.save(target_path + file.name, file)
            name = ''.join(random.choice(string.ascii_letters) for i in range(10))
            newFileName = name + ".mp4"
            newFileNamePath = target_path + newFileName
            os.rename(filenamepath, newFileNamePath)
            # Let's use Amazon S3
            # file_url = 'https://vozmee-assets.s3.amazonaws.com/'+newFileName
            file_url = 'https://d2eeirjdliqdth.cloudfront.net/' + newFileName
            s3 = boto3.resource("s3")
            bucket = s3.Bucket("vozmee-assets")
            # Print out bucket names
            bucket.upload_file(Key=newFileName, Filename=newFileNamePath,
                               ExtraArgs={'ContentType': "video/mp4"})
            # Amazon S3 bucket usage end
            videoModel.video_url = file_url
            origin_date = datetime.today()
            end_time = origin_date + timedelta(hours=24)
            videoModel.expiry_time = end_time
            videoModel.user_id = request.user.id
            videoModel.video_description = request.data['video_description']
            share_id = ''.join(random.choice(string.ascii_letters) for i in range(5))
            videoModel.share_id = share_id
            if music_id != "":
                videoModel.music_id = music_id
            videoModel.save()
            return JsonResponse({'message': 'Video uploaded successfully!', 'success': True, 'data': [], 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "Video uploading failed!", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def getUserVideos(request):
        try:
            id = request.user.id  # Fetching user id from JWT Token

            video_list = []
            cm_cursor = connection.cursor()
            cm_query = "SELECT vd.id,vd.video_url,vd.upload_time,vd.expiry_time,vd.user_id,vd.video_id,vd.video_description,vd.share_id, " \
                       "COALESCE(vs.total_comments,0) As total_comments,COALESCE(vs.total_likes,0) AS total_likes,COALESCE(vs.total_share,0) AS total_share, COALESCE(usrprof.profile_picture,'https://vozmee-assets.s3.amazonaws.com/defaultimage.jpeg') as profile_img, usrmgt.first_name, usrmgt.last_name, usrmgt.username, COALESCE(vs.total_views,0) AS total_views   " \
                       "FROM videos_videos vd " \
                       "left Join user_management_profile usrprof on usrprof.user_id = vd.user_id " \
                       "inner Join user_management_user usrmgt on usrmgt.id = vd.user_id " \
                       "FULL JOIN videos_summarymodel vs ON vd.video_id::text=vs.video_id WHERE vd.is_pending = '1' and vd.user_id= "+str(id)+" ORDER BY vd.id DESC "
            # data = Videos.objects.filter(user_id=id, is_pending=True)
            # if data:
            #     serializer = VideoSerializer(data, many=True)
            cm_cursor.execute(cm_query)
            cm_col_names = [col[0] for col in cm_cursor.description]
            for row in cm_cursor.fetchall():
                row_dict = dict(zip(cm_col_names, row))
                video_list.append(row_dict)
            final_video_list = []
            if video_list:
                if request.query_params.get('share_id'):
                    share_id = request.query_params.get('share_id')
                    for data in video_list:
                        if data['share_id'] == share_id:
                            final_video_list.append(data)
                    for data in video_list:
                        if data['share_id'] != share_id:
                            final_video_list.append(data)
                else:
                    final_video_list = video_list
                return JsonResponse(
                    {'message': 'User data fetched successfully', 'success': True, 'data': final_video_list,
                     'status': 200},
                    status=200)
            else:
                return JsonResponse({'message': 'No video found', 'success': True, 'data': [], 'status': 200},
                                    status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Internal Server Error', 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def downloadVideo(request):
        try:
            serializer = DownloadVideo(data=request.data)
            if serializer.is_valid():
                id = request.user.id
                video_url = request.data['video_url']
                data = Videos.objects.filter(user_id=id, video_url=video_url).values('video_url').first()
                if data is None:
                    data = {}
                return JsonResponse(
                    {'message': 'User data fetched successfully', 'success': True, 'data': data, 'status': 200},
                    status=200)
            else:
                return JsonResponse(
                    {'message': 'Enter a valid url please.', 'success': False, 'data': {}, 'status': 403}, status=403)
        except Exception as e:
            print(e)
            return JsonResponse({'message': statusList.error_not_found, 'success': False, 'data': {}, 'status': 500},
                                status=500)

    @staticmethod
    def commentVideo(request):
        try:
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                commentModel = Comments()
                video_id = request.data['video_id']
                commentModel.comment_body = request.data['comment_body']
                commentModel.video_id = video_id
                commentModel.user_id = request.user.id
                commentModel.save()
                summary = SummaryModel.objects.filter(video_id=video_id).first()
                if summary:
                    summary.total_comments = int(summary.total_comments) + 1
                    summary.updated_at = datetime.now()
                    summary.save()
                else:
                    summaryModel = SummaryModel()
                    summaryModel.video_id = video_id
                    summaryModel.total_comments = 1
                    summaryModel.save()
                return JsonResponse(
                    {'message': 'Comment added successfully.', 'success': True, 'data': [], 'status': 200},
                    status=200)
            else:
                return JsonResponse(
                    {'message': 'Enter a valid comment please.', 'success': False, 'data': [], 'status': 403},
                    status=403)
        except Exception as e:
            print(e)
            return JsonResponse(
                {'message': 'Could not comment on this video', 'success': False, 'data': [], 'status': 500}, status=500)

    @staticmethod
    def commentsList(request):
        try:
            serializer = videoSerializer(data=request)
            if serializer.is_valid():
                video_id = request['video_id']
                comment_list = []
                cm_cursor = connection.cursor()
                cm_query = "SELECT cm.id,cm.comment_body,cm.video_id,cm.user_id," \
                           "us.username,us.first_name, us.last_name,COALESCE(up.profile_picture,'https://vozmee-assets.s3.amazonaws.com/defaultimage.jpeg') as profile_img " \
                           "FROM videos_comments cm " \
                           "LEFT JOIN user_management_user us on us.id = cm.user_id " \
                           "LEFT JOIN user_management_profile up on up.user_id = us.id WHERE cm.video_id = '"+str(video_id)+"' ORDER BY cm.id DESC "
                cm_cursor.execute(cm_query)
                cm_col_names = [col[0] for col in cm_cursor.description]
                for row in cm_cursor.fetchall():
                    row_dict = dict(zip(cm_col_names, row))
                    comment_list.append(row_dict)
                if comment_list is not None:
                        return JsonResponse(
                            {'message': 'Comments list fetched successfully', 'success': True, 'data': comment_list,
                             'status': 200},
                            status=200)
                else:
                        return JsonResponse(
                            {'message': 'No comment found against this video', 'success': True, 'data': [],
                             'status': 200},
                            status=200)
            else:
                return JsonResponse({'message': 'Invalid video ID', 'success': False, 'data': [], 'status': 403},
                                    status=403)
        except Exception as e:
            print(e)
            return JsonResponse(
                {'message': 'Video comments could not fetch', 'success': False, 'data': [], 'status': 500}, status=500)

    @staticmethod
    def deleteComment(request):
        try:
            comment_id = request.data['comment_id']
            video_id = request.data['video_id']
            user_id = request.user.id
            comment = Comments.objects.filter(id=comment_id, video_id=video_id, user_id=user_id).first()
            if comment is not None:
                comment.delete()
                summary = SummaryModel.objects.filter(video_id=video_id).first()
                if summary:
                    summary.total_comments = int(summary.total_comments) - 1
                    summary.updated_at = datetime.now()
                    summary.save()
                return JsonResponse(
                    {'message': 'Comments deleted successfully', 'success': True, 'data': [],
                     'status': 200}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Comment could not delete', 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def deleteVideo(request):
        try:
            video_id = request.data['video_id']
            video = Videos.objects.filter(video_id=video_id).first()
            if video is not None:
                model = VideosHistory()
                model.video_url = video.video_url
                model.upload_time = video.upload_time
                model.expiry_time = video.expiry_time
                model.user_id = video.user_id
                model.video_delete_time = datetime.now()
                model.video_id = video.video_id
                model.video_description = video.video_description
                model.share_id = video.share_id
                model.music_id = video.music_id
                model.is_pending = video.is_pending
                model.save()

                s3 = boto3.client("s3")
                #bucket = s3.Bucket("vozmee-assets")
                video_ame = video.video_url.split('.net/')[1]
                response = s3.delete_objects(
                    Bucket="vozmee-assets",
                    Delete={"Objects": [{"Key": video_ame}]},
                )
                print("now delete video from s3 and table")
                video.delete()

                return JsonResponse(
                    {'message': 'video deleted successfully', 'success': True, 'data': [],
                     'status': 200}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'video could not delete', 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def likeVideo(request):
        try:
            serializer = LikeSerializer(data=request.data)
            if serializer.is_valid():
                video_id = request.data['video_id']
                is_like = request.data['is_like']
                like = Likes.objects.filter(video_id=video_id, user_id=request.user.id).first()
                msg = ""
                if like is None:
                    likeModel = Likes()
                    likeModel.is_like = True
                    likeModel.video_id = video_id
                    likeModel.user_id = request.user.id
                    likeModel.created_at = datetime.today()
                    likeModel.save()
                    summary = SummaryModel.objects.filter(video_id=video_id).first()
                    if summary is not None:
                        summary.total_likes = int(summary.total_likes) + 1
                        summary.updated_at = datetime.now()
                        summary.save()
                    else:
                        summaryModel = SummaryModel()
                        summaryModel.video_id = video_id
                        summaryModel.total_likes = 1
                        summaryModel.total_comments = 0
                        summaryModel.save()
                    msg = "Video liked successfully"
                else:
                    if like.is_like == False:
                        like.is_like = True
                        like.updated_at = datetime.now()
                        like.save()
                        summary = SummaryModel.objects.filter(video_id=video_id).first()
                        if summary is not None:
                            summary.total_likes = int(summary.total_likes) + 1
                            summary.updated_at = datetime.now()
                            summary.save()
                        msg = "Video liked successfully"

                    else:
                        like.is_like = False
                        like.updated_at = datetime.now()
                        like.save()
                        summary = SummaryModel.objects.filter(video_id=video_id).first()
                        if summary is not None:
                            summary.total_likes = int(summary.total_likes) - 1
                            summary.updated_at = datetime.now()
                            summary.save()
                        msg = "Video unliked successfully"

                return JsonResponse({'message': msg, 'success': True, 'data': [], 'status': 200},
                                    status=200)
            else:
                return JsonResponse(
                    {'message': 'Enter a valid url please.', 'success': False, 'data': [], 'status': 403}, status=403)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'User could not like video', 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def likesList(request):
        try:
            serializer = videoSerializer(data=request)
            if serializer.is_valid():
                video_id = request['video_id']
                videos = Likes.objects.filter(video_id=video_id, is_like=True)
                if videos:
                    likes_list = []
                    for item in videos:
                        name = User.objects.filter(id=item.user_id).first()
                        if name:
                            context = {'id': item.id, 'is_like': item.is_like, 'user_id': item.user_id,
                                       'first_name': name.first_name, 'last_name': name.last_name}
                            likes_list.append(context)
                        else:
                            context = {'id': item.id, 'is_like': item.is_like, 'user_id': item.user_id,
                                       'first_name': "", 'last_name': ""}
                            print(context)
                            likes_list.append(context)

                    if likes_list:
                        return JsonResponse(
                            {'message': 'Likes list fetched successfully', 'success': True, 'data': likes_list,
                             'status': 200},
                            status=200)
                    else:
                        return JsonResponse(
                            {'message': 'No likes found against this video', 'success': True, 'data': [],
                             'status': 200},
                            status=200)
                else:
                    return JsonResponse(
                        {'message': 'No likes found against this video', 'success': True, 'data': [], 'status': 200},
                        status=200)
            else:
                return JsonResponse({'message': 'Invalid video ID', 'success': False, 'data': [], 'status': 403},
                                    status=403)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'User likes could not fetch', 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def statsSummary(request):
        try:
            video_id = request['video_id']
            video_summary = SummaryModel.objects.filter(video_id=video_id).first()
            if video_summary:
                serializer = SummarySerializer(video_summary)
                return JsonResponse(
                    {'message': 'Summary for video fetched successfully', 'success': True, 'data': serializer.data,
                     'status': 200},
                    status=200)
            else:
                return JsonResponse(
                    {'message': 'No record found against this video', 'success': True, 'data': {}, 'status': 200},
                    status=200)
        except Exception as e:
            print(e)
            return JsonResponse(
                {'message': 'Summary for this video could not fetch', 'success': False, 'data': {}, 'status': 500},
                status=500)

    @staticmethod
    def getAllVideos(request):
        try:
            limit = request.data['limit']
            offset = request.data['offset']
            video_list = []
            cm_cursor = connection.cursor()
            cm_query = "SELECT vd.id,vd.video_url,vd.upload_time,vd.expiry_time,vd.user_id,vd.video_id,vd.video_description,vd.share_id, " \
                       "COALESCE(vs.total_comments,0) As total_comments,COALESCE(vs.total_likes,0) AS total_likes,COALESCE(vs.total_share,0) AS total_share, COALESCE(usrprof.profile_picture,'https://vozmee-assets.s3.amazonaws.com/defaultimage.jpeg') as profile_img, usrmgt.first_name, usrmgt.last_name, usrmgt.username, COALESCE(vs.total_views,0) AS total_views  " \
                       "FROM videos_videos vd " \
                       "left Join user_management_profile usrprof on usrprof.user_id = vd.user_id " \
                       "inner Join user_management_user usrmgt on usrmgt.id = vd.user_id " \
                       "FULL JOIN videos_summarymodel vs ON vd.video_id::text=vs.video_id WHERE vd.is_pending = '1' ORDER BY vd.id DESC LIMIT " + str(
                limit) + " OFFSET " + str(offset)
            cm_cursor.execute(cm_query)
            cm_col_names = [col[0] for col in cm_cursor.description]
            for row in cm_cursor.fetchall():
                row_dict = dict(zip(cm_col_names, row))
                video_list.append(row_dict)
            final_video_list = []
            if video_list:
                if request.query_params.get('share_id'):
                    share_id = request.query_params.get('share_id')
                    for data in video_list:
                        if data['share_id'] == share_id:
                            final_video_list.append(data)
                    for data in video_list:
                        if data['share_id'] != share_id:
                            final_video_list.append(data)
                else:
                    final_video_list = video_list
                return JsonResponse(
                    {'message': 'Videos fetched successfully', 'success': True, 'data': final_video_list,
                     'status': 200},
                    status=200)
            else:
                return JsonResponse({'message': 'No video found', 'success': True, 'data': [], 'status': 200},
                                    status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Videos could not fetch', 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def uploadMusic(request):
        try:
            musicModel = Music()
            fs = FileSystemStorage()
            file = request.data['file']
            target_path = 'myMusic/'
            filenamepath = fs.save(target_path + file.name, file)
            # local_file_url = fs.url(filename)
            name = ''.join(random.choice(string.ascii_letters) for i in range(10))
            newFileName = name + ".mp3"
            newFileNamePath = target_path + newFileName
            os.rename(filenamepath, newFileNamePath)
            # Let's use Amazon S3
            file_url = 'https://vozmee-assets.s3.amazonaws.com/' + newFileName
            s3 = boto3.resource("s3")
            bucket = s3.Bucket("vozmee-assets")
            # Print out bucket names
            bucket.upload_file(Key=newFileName, Filename=newFileNamePath,
                               ExtraArgs={'ContentType': "audio/mp3"})
            # Amazon S3 bucket usage end
            musicModel.music_url = file_url
            musicModel.name = newFileName
            musicModel.save()
            # if os.path.isfile(newFileNamePath):
            #     os.remove(newFileNamePath)
            return JsonResponse({'message': 'Music uploaded successfully!', 'success': True, 'data': [], 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "Music uploading failed!", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def GetMusicList(request):
        try:
            data = Music.objects.all()
            if data:
                serializer = MusicSerializer(data, many=True)
                return JsonResponse(
                    {'message': 'Music list fetched successfully', 'success': True, 'data': serializer.data,
                     'status': 200},
                    status=200)
            else:
                return JsonResponse({'message': 'No music found', 'success': True, 'data': [], 'status': 200},
                                    status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Music list could not fetch', 'success': False, 'data': [], 'status': 500},
                                status=500)


    @staticmethod
    def addView(request):
        try:
            viewModel = Views()
            user_id = request.user.id
            video_id = request.data['video_id']
            views = Views.objects.filter(user_id = user_id, video_id = video_id).first()
            if views is None:
                viewModel.user_id = user_id
                viewModel.video_id = video_id
                viewModel.save()
                viewCount = SummaryModel.objects.filter(video_id = video_id).first()
                if viewCount is not None:
                    viewCount.total_views = int(viewCount.total_views) + 1
                    viewCount.updated_at = datetime.now()
                    viewCount.save()
                else:
                    viewSummary = SummaryModel()
                    viewSummary.video_id = video_id
                    viewSummary.total_comments = 0
                    viewSummary.total_likes = 0
                    viewSummary.total_share = 0
                    viewSummary.total_views = 1
                    viewSummary.save()
                return JsonResponse({'message': 'View added successfully!','success': True, 'data': [],'status':200},
                                    status=200)
            else:
                return JsonResponse({'message': 'View already exists!','success': True, 'data': [],'status':200},
                                    status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'View could not add', 'success': False, 'data': [], 'status': 500}, status=500)