from main.models import LatestPost, Comment
from django.contrib.auth import get_user_model
from rest_framework import serializers


class LatestPostSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    author = serializers.ReadOnlyField()
    score = serializers.ReadOnlyField()
    descendants = serializers.ReadOnlyField()
    time = serializers.ReadOnlyField()
    slug = serializers.ReadOnlyField()

    class Meta:
        model = LatestPost
        fields = [
            "url",
            "id",
            "title",
            "post_type",
            "author",
            "slug",
            "text",
            "dead",
            "post_url",
            "score",
            "descendants",
            "created_by",
            "time",
        ]


class UserPostSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, view_name="user-detail", read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["url", "id", "username", "posts"]


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    post = serializers.SlugRelatedField(slug_field="id", queryset=LatestPost.objects.all())
    author = serializers.ReadOnlyField()
    score = serializers.ReadOnlyField()
    time = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = [
            "url",
            "id",
            "title",
            "post",
            "author",
            "text",
            "dead",
            "comment_url",
            "score",
            "time",
        ]
