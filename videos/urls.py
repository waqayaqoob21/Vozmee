from django.urls import path
from videos.views import *

urlpatterns = [
    path('UploadVideo', UploadVideoAPIVIEW.as_view(), name='UploadVideo'),
    path('GetUserVideos', GetUserVideosAPIVIEW.as_view(), name='GetUserVideos'),
    path('DownloadVideo', DownloadVideoAPIVIEW.as_view(), name='DownloadVideo'),
    path('AddComment', CommentAPIVIEW.as_view(), name='AddComment'),
    path('GetCommentsList', GetVideoCommentsListAPIVIEW.as_view(), name='GetCommentsList'),
    path('DeleteComment', DeleteCommentAPIVIEW.as_view(), name='DeleteComment'),
    path('LikeUnlike', LikeAPIVIEW.as_view(), name='LikeUnlike'),
    path('GetLikesList', GetVideoLikesListAPIVIEW.as_view(), name='GetLikesList'),
    path('GetSummary', GetVideoStatsSummayAPIVIEW.as_view(), name='GetSummary'),
    path('GetAllVideos', GetAllVideosAPIVIEW.as_view(), name='GetAllVideos'),
    path('DeleteVideo', DeleteVideoAPIVIEW.as_view(), name='DeleteVideo'),

    # path('UploadMusic', UploadMusicAPIVIEW.as_view(), name='UploadMusic'),
    path('GetMusicList', GetMusicListAPIVIEW.as_view(), name='GetMusicList'),
    path('AddView', AddViewsAPIVIEW.as_view(), name='AddView'),

]