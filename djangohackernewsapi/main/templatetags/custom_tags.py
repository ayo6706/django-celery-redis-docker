from main.models import Comment, LatestPost
from django import template

register = template.Library()


@register.filter
def post_title(parent_id):
    comm = LatestPost.objects.filter(unique_api_post_id=parent_id).first()
    if comm:
        if comm.post_type == "comment":
            comm2 = LatestPost.objects.filter(unique_api_post_id=comm.parent_id).first()
            if comm2:
                return comm2.title
        return comm.title
    else:
        return "Parent post has not been fetched yet"


@register.filter
def post_url(parent_id):
    comm = LatestPost.objects.filter(unique_api_post_id=parent_id).first()
    if comm:
        if comm.post_type == "comment":
            comm2 = LatestPost.objects.filter(unique_api_post_id=comm.parent_id).first()
            if comm2:
                return comm2.get_absolute_url()
        return comm.get_absolute_url()
    else:
        return "#"
