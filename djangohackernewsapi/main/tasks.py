import dateutil.parser
import datetime
import requests
from celery import shared_task
from django.template.defaultfilters import slugify
from .models import LatestPost, Comment

HACKER_NEWS_API_URL = "https://hacker-news.firebaseio.com/v0"


def get_item(id):
    item = requests.get(f"{HACKER_NEWS_API_URL}/item/{id}.json")
    return item.json()


@shared_task
def get_and_store_post_comments(unique_api_post_id, post_id):
    single_post = get_item(unique_api_post_id)
    post = LatestPost.objects.get(id=post_id, unique_api_post_id=unique_api_post_id)
    for kid in single_post.get("kids", []):
        comment_response = get_item(kid)
        comment, _ = Comment.objects.get_or_create(unique_comment_api_id=kid, id=post.id)
        comment.post = post
        comment.post_type = comment_response.get("type", "")
        comment.author = comment_response.get("by", "")
        comment.time = dateutil.parser.parse(
            datetime.datetime.fromtimestamp(comment_response.get("time", 0)).strftime("%Y-%m-%d %H:%M:%S")
        )
        comment.text = comment_response.get("text", "")
        comment.comment_url = comment_response.get("url", "")
        comment.score = comment_response.get("score", 0)
        comment.save()


def get_max_item_id():
    max_item_id = requests.get(f"{HACKER_NEWS_API_URL}/maxitem.json")
    return max_item_id.json()


@shared_task
def store_latest_posts():
    max_item_id = get_max_item_id()
    for sid in reversed(range(max_item_id)):
        post_response = get_item(sid)
        post, _ = LatestPost.objects.get_or_create(
            unique_api_post_id=sid,
            title=post_response.get(
                "title", f"No title for this {post_response.get('type', 'No type')} from the API"
            ),
        )
        post.post_type = post_response.get("type", "No type")
        post.author = post_response.get("by", "No creator")
        post.time = dateutil.parser.parse(
            datetime.datetime.fromtimestamp(post_response.get("time", 0)).strftime("%Y-%m-%d %H:%M:%S")
        )
        post.slug = slugify(
            post_response.get("title", f"No title for this {post_response.get('type', 'No type')} from the API")
        )
        post.post_url = post_response.get("url", "")
        post.text = post_response.get("text", "")
        post.score = post_response.get("score", 0)
        post.descendants = post_response.get("descendants", 0)
        post.parent_id = post_response.get("parent", -1)
        post.save()
        get_and_store_post_comments.delay(unique_api_post_id=post.unique_api_post_id, post_id=post.id)



@shared_task
def get_latest_posts():
    store_latest_posts.delay()
