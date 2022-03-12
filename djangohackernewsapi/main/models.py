from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid


# Create your models here.
class LatestPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unique_api_post_id = models.IntegerField("post id", null=True)
    post_type = models.CharField("Type of item", max_length=15, null=True)
    author = models.CharField("Author", max_length=50, null=True)
    slug = models.SlugField(max_length=2000, null=True)
    text = models.TextField("The comment, post or poll text.", null=True)
    dead = models.BooleanField(default=False)
    post_url = models.URLField("URL", max_length=1000, null=True)
    score = models.IntegerField("Score", null=True)
    descendants = models.IntegerField("Descendants", null=True)
    title = models.TextField("Title", null=True)
    parent_id = models.IntegerField("Parent ID", null=True)
    created_by = models.ForeignKey(get_user_model(), related_name="posts", on_delete=models.CASCADE, null=True)
    time = models.DateTimeField("Date created", null=True)

    class Meta:
        unique_together = ("unique_api_post_id", "title")
        verbose_name = "Latest post"
        verbose_name_plural = "Latest posts"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:post_detail", kwargs={"id": self.id, "slug": self.slug})


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unique_comment_api_id = models.IntegerField("post ID", null=True, unique=True)
    post = models.ForeignKey(LatestPost, on_delete=models.CASCADE, related_name="comments", null=True)
    author = models.CharField("Author", max_length=50, null=True)
    time = models.DateTimeField("Date created", null=True)
    text = models.TextField("Text", null=True)
    dead = models.BooleanField(default=False)
    comment_url = models.URLField("URL", max_length=1000, null=True)
    score = models.IntegerField("Score", null=True)
    title = models.TextField("Title", null=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.post.title

