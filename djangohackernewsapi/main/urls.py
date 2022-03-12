from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("lazy_load_posts/", views.lazy_load_posts, name="lazy_load_posts"),
    path("filter_by_story_type/", views.filter_by_post_type, name="filter_by_post_type"),
    path("search_by_text/", views.search_by_text, name="search_by_text"),
    path("story-detail/<uuid:id>/<slug:slug>/", views.post_detail, name="post_detail"),
]
