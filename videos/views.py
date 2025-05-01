from drf_yasg import openapi
from rest_framework.views import APIView
from videos.videoController import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
# Create your views here.

ctrlObj = VideoController()

class UploadVideoAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    # @swagger_auto_schema(
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         required=['banner'],
    #         properties={
    #             'category': openapi.Schema(type=openapi.TYPE_STRING),
    #             'name': openapi.Schema(type=openapi.TYPE_STRING),
    #             'location': openapi.Schema(type=openapi.TYPE_STRING),
    #             'start_date': openapi.Schema(type=openapi.TYPE_STRING, default="yyyy-mm-dd"),
    #             'end_date': openapi.Schema(type=openapi.TYPE_STRING, default='yyyy-mm-dd'),
    #             'description': openapi.Schema(type=openapi.TYPE_STRING),
    #             'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
    #             'banner': openapi.Schema(type=openapi.TYPE_FILE,),
    #         },
    #     ),
    #     operation_description='Create an events'
    # )

    @swagger_auto_schema(
        operation_description='Upload file...',
        manual_parameters=[openapi.Parameter('file', openapi.IN_FORM,
                                             type=openapi.TYPE_FILE,
                                             required = True,
                                            description='File to be uploaded'),
                           openapi.Parameter('video_description', openapi.IN_FORM, type=openapi.TYPE_STRING,required = True,
                                             description='Discription of video'),
                           openapi.Parameter('music_id', openapi.IN_FORM, type=openapi.TYPE_STRING,
                                             description='Music ID')
                           ],

    )

    def post(self, request):
        result = ctrlObj.uploadVideo(request)
        return result

class GetUserVideosAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = ctrlObj.getUserVideos(request)
        return result

class DownloadVideoAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=DownloadVideo,
        operation_description="Download Video",
    )
    def post(self, request):
        result = ctrlObj.downloadVideo(request)
        return result

class CommentAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        # manual_parameters=[openapi.Parameter("video_id",
        #                                      openapi.IN_QUERY,
        #                                      description="Video ID",
        #                                      type=openapi.TYPE_STRING,
        #                                      required=['video_id'],
        #
        #                                      )],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['comment_body','video_id'],
            properties={
                'comment_body': openapi.Schema(type=openapi.TYPE_STRING),
                'video_id': openapi.Schema(type=openapi.TYPE_STRING),

            },
        ),
        operation_description='Enter your comment'
    )

    def post(self, request):
        result = ctrlObj.commentVideo(request)
        return result

class GetVideoCommentsListAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['video_id'],
            properties={
                'video_id': openapi.Schema(type=openapi.TYPE_STRING),

            },
        ),
        operation_description='Enter your comment'
    )
    def post(self, request):
        result = ctrlObj.commentsList(request.data)
        return result

class DeleteCommentAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['comment_id','comment_body','video_id'],
            properties={
                'comment_id': openapi.Schema(type=openapi.TYPE_STRING),
                'video_id': openapi.Schema(type=openapi.TYPE_STRING),

            },
        ),
        operation_description='Enter your comment'
    )

    def post(self, request):
        result = ctrlObj.deleteComment(request)
        return result


class DeleteVideoAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['video_id'],
            properties={
                'video_id': openapi.Schema(type=openapi.TYPE_STRING),

            },
        )
    )

    def post(self, request):
        result = ctrlObj.deleteVideo(request)
        return result

class LikeAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        # manual_parameters=[openapi.Parameter("video_id",
        #                                      openapi.IN_QUERY,
        #                                      description="Video ID",
        #                                      type=openapi.TYPE_STRING,
        #                                      required=['video_id'],
        #
        #                                      )],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['is_like', 'video_id'],
            properties={
                'is_like': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'video_id': openapi.Schema(type=openapi.TYPE_STRING),

            },
        ),
        operation_description='Like video'
    )
    def post(self, request):
        result = ctrlObj.likeVideo(request)
        return result

class GetVideoLikesListAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['video_id'],
            properties={
                'video_id': openapi.Schema(type=openapi.TYPE_STRING),

            },
        ),
        operation_description='Video Likes'
    )
    def post(self, request):
        result = ctrlObj.likesList(request.data)
        return result


class GetVideoStatsSummayAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['video_id'],
            properties={
                'video_id': openapi.Schema(type=openapi.TYPE_STRING),

            },
        ),
        operation_description='Enter video summary'
    )
    def post(self, request):
        result = ctrlObj.statsSummary(request.data)
        return result


class GetAllVideosAPIVIEW(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter("share_id",
                                             openapi.IN_QUERY,
                                             description="Share ID (Optional)",
                                             type=openapi.TYPE_STRING,
                                             )],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['limit', 'offset'],
            properties={
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                'offset': openapi.Schema(type=openapi.TYPE_INTEGER),

            },
        ),
        operation_description='Enter video summary'
    )
    def post(self, request):
        result = ctrlObj.getAllVideos(request)
        return result


class UploadMusicAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        operation_description='Upload file...',
        manual_parameters=[openapi.Parameter('file', openapi.IN_FORM,
                                             type=openapi.TYPE_FILE,
                                            description='File to be uploaded')])
    def post(self, request):
        result = ctrlObj.uploadMusic(request)
        return result

class GetMusicListAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        result = ctrlObj.GetMusicList(request)
        return result


class AddViewsAPIVIEW(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['video_id'],
            properties={
                'video_id': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        operation_description='Add Video'
    )
    def post(self, request):
        result = ctrlObj.addView(request)
        return result