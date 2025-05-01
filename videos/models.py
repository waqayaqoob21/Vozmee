from django.db import models
import uuid
# Create your models here.
class Videos(models.Model):
    id = models.AutoField(primary_key=True)
    video_url = models.TextField()
    upload_time = models.DateTimeField(auto_now_add=True)
    expiry_time = models.DateTimeField()
    user_id = models.IntegerField()
    video_id = models.UUIDField(default=uuid.uuid4, editable=False, max_length=8)
    video_description = models.TextField(null=True)
    share_id = models.CharField(max_length=5,null=True)
    music_id =  models.CharField(max_length=50,null=True)
    is_pending = models.BooleanField(default=False)


class VideosHistory(models.Model):
    id = models.AutoField(primary_key=True)
    video_url = models.TextField()
    upload_time = models.DateTimeField()
    expiry_time = models.DateTimeField()
    user_id = models.IntegerField()
    video_delete_time = models.DateTimeField(auto_now_add=True)
    video_id = models.UUIDField(default=uuid.uuid4, editable=False, max_length=8)
    video_description = models.TextField(null=True)
    share_id = models.CharField(max_length=5,null=True)
    music_id =  models.CharField(max_length=50,null=True)
    is_pending = models.BooleanField(default=False)

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    comment_body = models.TextField()
    video_id = models.CharField(max_length=50)
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Likes(models.Model):
    id = models.AutoField(primary_key=True)
    is_like = models.BooleanField(default=False)
    video_id = models.CharField(max_length=50)
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True)

class SummaryModel(models.Model):
    id = models.AutoField(primary_key=True)
    video_id = models.CharField(max_length=50)
    total_comments = models.IntegerField()
    total_likes = models.IntegerField(default=0)
    total_share = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True)
    total_views = models.IntegerField(default=0)

class Music(models.Model):
    id = models.AutoField(primary_key=True)
    music_url = models.TextField()
    name = models.CharField(max_length=50)
    music_id = models.UUIDField(default=uuid.uuid4, editable=False, max_length=8)

class Views(models.Model):
    id = models.AutoField(primary_key = True)
    video_id = models.CharField(max_length=50)
    user_id = models.IntegerField()
    viewed_at = models.DateTimeField(auto_now_add=True)