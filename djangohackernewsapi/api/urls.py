from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path("", views.api_root),
    path("latest-posts/", views.PostList.as_view(), name="latestpost-list"),
    path("latest-posts/<uuid:pk>/", views.PostDetail.as_view(), name="latestpost-detail"),
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    path("comments/", views.CommentList.as_view(), name="comment-list"),
    path("comments/<uuid:pk>/", views.CommentDetail.as_view(), name="comment-detail"),

]

urlpatterns = format_suffix_patterns(urlpatterns)
