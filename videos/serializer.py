from rest_framework import serializers
from .models import *
from rest_framework.serializers import Serializer
from rest_framework.fields import CharField, IntegerField, DateTimeField, BooleanField, UUIDField


class VideoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Videos
        fields = '__all__'

class DownloadVideo(Serializer):
    video_url = CharField()

class CommentSerializer(Serializer):
    comment_body = CharField()
    video_id = CharField()


class LikeSerializer(Serializer):
    is_like = BooleanField()

class videoSerializer(Serializer):
    video_id = UUIDField()
class SummarySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = SummaryModel
        fields = '__all__'

class MusicSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Music
        fields = '__all__'