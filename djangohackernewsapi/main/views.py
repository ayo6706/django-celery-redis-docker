from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from .models import Comment, LatestPost
from . import utils


def index(request):
    posts = LatestPost.objects.all().order_by("-time")[:4]
    types = LatestPost.objects.order_by("-post_type").values_list("post_type")
    post_types = []
    for t in types:
        if t[0] in post_types:
            continue
        post_types.append(t[0])
    context = {"page_title": "Welcome to a Beautiful Hackernews clone", "posts": posts, "post_types": post_types}
    return render(request, "main/index.html", context)


def post_detail(request, id, slug):
    post = get_object_or_404(LatestPost, id=id, slug=slug)
    comments_by_parent_id = LatestPost.objects.filter(unique_api_post_id=post.parent_id)
    comments_normally = Comment.objects.select_related("post").filter(post=post)
    from itertools import chain

    post_comments = list(chain(comments_by_parent_id, comments_normally))
    context = {
        "page_title": f"{post.title}",
        "post": post,
        "post_comments": post_comments,
    }
    return render(request, "main/detail.html", context)


def lazy_load_posts(request):
    post = LatestPost.objects.all().order_by("-time")
    """
    Exposes data for easy lazy-loading at the frontend
    """
    page = request.POST.get("page")
    results_per_page = 4
    paginator = Paginator(post, results_per_page)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(2)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    posts_html = loader.render_to_string("main/posts.html", {"posts": posts})
    output_data = {
        "posts_html": posts_html,
        "has_next": posts.has_next(),
        "posts_count": len(posts),
    }
    return JsonResponse(output_data)


def search_by_text(request):
    if request.method == "POST":
        search_text = request.POST.get("search_text")
        posts = utils.postss(search_text).get("posts", [])
        if len(posts) > 4:
            page = request.POST.get("page")
            results_per_page = 4
            paginator = Paginator(posts, results_per_page)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(2)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            posts_html = loader.render_to_string("main/posts.html", {"posts": posts})
            posts_list = []
            for i in posts:
                posts_list.append({"title": i.title, "author": i.author, "post_type": i.post_type, "text": i.text})
            output_data = {
                "posts_html": posts_html,
                "has_next": posts.has_next(),
                "posts_count": len(posts),

            }
            return JsonResponse(output_data)
        elif len(posts) < 4 and len(posts) > 0:
            posts_html = loader.render_to_string("main/posts.html", {"posts": posts})
            posts_list = []
            for i in posts:
                posts_list.append({"title": i.title, "author": i.author, "post_type": i.post_type, "text": i.text})
            output_data = {
                "posts_html": posts_html,
                "has_next": False,
                "posts_count": len(posts),

            }
            return JsonResponse(output_data)
        else:
            return JsonResponse({"no_post": True})
    if request.method == "GET":
        search_text = request.GET.get("search_text")
        posts = utils.posts(search_text).get("posts", [])
        if len(posts) > 4:
            page = request.GET.get("page")
            results_per_page = 4
            paginator = Paginator(posts, results_per_page)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            posts_html = loader.render_to_string("main/posts.html", {"posts": posts})
            posts_list = []
            for i in posts:
                posts_list.append({"title": i.title, "author": i.author, "post_type": i.post_type, "text": i.text})
            output_data = {
                "posts_html": posts_html,
                "has_next": posts.has_next(),
                "posts_count": len(posts),
                # "real_posts": posts_list,
            }
            return JsonResponse(output_data)
        elif len(posts) < 4 and len(posts) > 0:
            posts_html = loader.render_to_string("main/posts.html", {"posts": posts})
            posts_list = []
            for i in posts:
                posts_list.append({"title": i.title, "author": i.author, "post_type": i.post_type, "text": i.text})
            output_data = {
                "posts_html": posts_html,
                "has_next": False,
                "posts_count": len(posts),

            }
            return JsonResponse(output_data)
        else:
            return JsonResponse({"no_post": True})


def filter_by_post_type(request):
    if request.method == "POST":
        post_type = request.POST["post_type"]
        posts = LatestPost.objects.filter(post_type=post_type).order_by("-time")
        if len(posts) > 4:
            page = request.POST.get("page")
            results_per_page = 4
            paginator = Paginator(posts, results_per_page)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(2)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            posts_html = loader.render_to_string("main/posts.html", {"posts": posts})
            output_data = {
                "posts_html": posts_html,
                "has_next": posts.has_next(),
                "posts_count": len(posts),
            }
            return JsonResponse(output_data)
        elif len(posts) < 4 and len(posts) > 0:
            posts_html = loader.render_to_string("main/posts.html", {"posts": posts})
            output_data = {
                "posts_html": posts_html,
                "has_next": False,
                "posts_count": len(posts),
            }
            return JsonResponse(output_data)
        else:
            return JsonResponse({"no_post": True})
    elif request.method == "GET":
        post_type = request.GET["post_type"]
        posts = LatestPost.objects.filter(post_type=post_type).order_by("-time")
        if len(posts) > 4:
            paginator = Paginator(posts, 4)
            page = request.GET.get("page")
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer deliver the first page
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            newposts_html = loader.render_to_string("main/posts.html", {"posts": posts})
            output_data = {
                "newposts_html": newposts_html,
                "newhas_next": posts.has_next(),
                "newposts_count": len(posts),
            }
            return JsonResponse(output_data)
        elif len(posts) < 4 and len(posts) > 0:
            newposts_html = loader.render_to_string("main/posts.html", {"posts": posts})
            output_data = {
                "newposts_html": newposts_html,
                "newhas_next": False,
                "newposts_count": len(posts),
            }
            return JsonResponse(output_data)
        else:
            return JsonResponse({"no_post": True})

