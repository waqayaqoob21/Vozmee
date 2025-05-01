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
import os,shutil
import random
import string
from django.db import connection
from moviepy.editor import *


def my_scheduled_job_delete():
    try:
        now = datetime.now() # 5 days ago
        vidoeModel = Videos.objects.filter(expiry_time__lt=now)
        if vidoeModel is not None:
            for obj in vidoeModel:
                video_name = obj.video_url
                video_id = obj.video_id
                video_likes = Likes.objects.filter(video_id = video_id)
                if video_likes is not None:
                    for like in video_likes:
                        like.delete()
                video_comments = Comments.objects.filter(video_id = video_id)
                if video_comments is not None:
                    for comment in video_comments:
                        comment.delete()
                video_summary = SummaryModel.objects.filter(video_id = video_id)
                if video_summary is not None:
                    video_summary.delete()
                video_name = video_name.split(".net/")[1]
                print(video_name)
                s3 = boto3.resource('s3')
                s3.Object('vozmee-assets', video_name).delete()
                obj.delete()
            return JsonResponse(
                {'message': 'video deleted successfully', 'success': True, 'data': [], 'status': 200},
                status=200)
        else:
            return JsonResponse(
                {'message': 'No video is to be deleted', 'success': True, 'data': [], 'status': 200},
                status=200)
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'Music list could not fetch', 'success': False, 'data': [], 'status': 500},
                            status=500)
def editVideoCronJob():
    try:
        print("helloo")
        fs = FileSystemStorage()
        pendingVideos = Videos.objects.filter(is_pending=False)
        music_name = ""
        music_id = ""
        video_id = ""
        if pendingVideos.exists():
            for curr_video in pendingVideos:
                if curr_video is not None:
                    if curr_video.music_id is not None:
                        music_id = curr_video.music_id
                        music = Music.objects.filter(music_id=music_id).first()
                        if music is not None:
                            music_name = music.name
                        else:
                            music_name = ""
                file_url = curr_video.video_url
                video_id = curr_video.id
                video_name = file_url.split('.net/')[1]
                # target_path = '/home/ubuntu/LoopServiceBackend/myVideos/'
                target_path = '/home/waqar/Documents/GitHub/Vozmee/loop-backend/loopService/myVideos/'
                print(target_path)
                newFileName = ""
                newFileNamePath = ""
                videoFileNamePath = target_path + video_name
                video_to_resize = VideoFileClip(videoFileNamePath)
                video_width = video_to_resize.w
                video_height = video_to_resize.h
                video_duration = video_to_resize.duration
                video = ""
                if video_duration > 30.0:
                    video = video_to_resize.set_duration(29.9)
                    if os.path.isfile(videoFileNamePath):
                        oldFIlePath = target_path + "oldFile.mp4"
                        os.rename(videoFileNamePath, oldFIlePath)
                    video = video.write_videofile(videoFileNamePath)
                if video_width != 480 or video_height != 864:
                    if video == '':
                        video = video_to_resize
                    video = video.resize((480, 864))
                    video.write_videofile(target_path + "resized_video.mp4")
                else:
                    video = VideoFileClip(videoFileNamePath)
                if music_id is not '':
                    # musicFileNamePath = "/home/ubuntu/LoopServiceBackend/myMusic/" + music_name
                    musicFileNamePath = "/home/waqar/Documents/GitHub/Vozmee/loop-backend/loopService/myMusic/" + music_name
                    music = AudioFileClip(musicFileNamePath)
                    audio_duaration = music.duration
                    if audio_duaration < video_duration:
                        music = afx.audio_loop(music, duration=video_duration)
                        audio_duaration = music.duration
                    if video_duration <= 30.0 and audio_duaration >= video_duration:
                        new_music = music.set_duration(video_duration)
                        final_video = video.set_audio(new_music)
                        final_video.write_videofile(target_path + "final_video.mp4")
                        if os.path.isfile(target_path + "resized_video.mp4"):
                            os.remove(target_path + "resized_video.mp4")
                        curr_target_path = target_path + "final_video.mp4"
                        if os.path.isfile(videoFileNamePath):
                            os.remove(videoFileNamePath)
                        newFileNamePath = target_path + video_name
                        os.rename(curr_target_path, newFileNamePath)

                newFileNamePath = target_path + video_name
                os.rename(videoFileNamePath, newFileNamePath)
                # Let's use Amazon S3
                file_url = 'https://vozmee-assets.s3.amazonaws.com/' + video_name
                print(file_url)
                s3 = boto3.resource("s3")
                s3.Object('vozmee-assets', video_name).delete()
                bucket = s3.Bucket("vozmee-assets")
                # Print out bucket names
                bucket.upload_file(Key=video_name, Filename=newFileNamePath,
                                   ExtraArgs={'ContentType': "video/mp4"})
                if os.path.isfile(newFileNamePath):
                    os.remove(newFileNamePath)
                    if os.path.isfile(target_path + "resized_video.mp4"):
                        os.remove(target_path + "resized_video.mp4")
                    if os.path.isfile(target_path + "oldFile.mp4"):
                        os.remove(target_path + "oldFile.mp4")
                    curr_video.is_pending = True
                    curr_video.save()
        print("Cron Job ran successfully!")
        return JsonResponse(
            {'message': 'videos uploaded successfully', 'success': True, 'data': [], 'status': 200},
            status=200)
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'Music list could not fetch', 'success': False, 'data': [], 'status': 500},
                            status=500)