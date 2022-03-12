from main.models import LatestPost, Comment

from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework import permissions
from django.template.defaultfilters import slugify
from django.utils import timezone

from .permissions import IsOwner
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CommentSerializer, LatestPostSerializer, UserPostSerializer


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "stories": reverse("latestpost-list", request=request, format=format),
            "users": reverse("user-list", request=request, format=format),
            "comments": reverse("comment-list", request=request, format=format),
        }
    )


class PostList(generics.ListCreateAPIView):
    queryset = LatestPost.objects.all().order_by("-time")
    serializer_class = LatestPostSerializer

    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "author"]
    filterset_fields = [
        "post_type",
        "author",
        "text",
    ]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            slug=slugify(self.request.data["title"]),
            time=timezone.now(),
            author=self.request.user.username,
            score=0,
            post_type=self.request.data["post_type"].lower(),
        )


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LatestPost.objects.all()
    serializer_class = LatestPostSerializer

    permission_classes = (permissions.IsAuthenticated, IsOwner,)



class UserList(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserPostSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserPostSerializer


class CommentList(generics.ListAPIView):
    queryset = Comment.objects.select_related("post").order_by("-time")
    serializer_class = CommentSerializer

    permission_classes = (permissions.IsAuthenticated,)


    def perform_create(self, serializer):
        serializer.save(author=self.request.user.username, score=0)


class CommentDetail(generics.RetrieveAPIView):
    queryset = Comment.objects.select_related("post").order_by("-time")
    serializer_class = CommentSerializer

    permission_classes = (permissions.IsAuthenticated, IsOwner,)

