from django.contrib import admin
from .models import LatestPost, Comment

# Register your models here.


@admin.register(LatestPost)
class LatestPostAdmin(admin.ModelAdmin):
    list_display = ["unique_api_post_id", "post_type", "author", "title", "post_url", "parent_id"]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title", "post_type", "author", "created_by", "unique_api_post_id"]
    list_per_page = 20
    list_filter = [
        "post_type",
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["unique_comment_api_id", "author", "title", "comment_url"]
    list_per_page = 20
