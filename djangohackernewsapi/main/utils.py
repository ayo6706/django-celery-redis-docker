from django.db.models import Q

from .models import LatestPost

STRIP_WORDS = ["a", "an", "and",  "or", "that", "the", "by", "for", "from", "in", "no", "not", "of", "on", "to", "with"]


def postss(search_text):
    words = _prepare_words(search_text)
    posts = LatestPost.objects.all()
    results = {}
    results["posts"] = []
    # iterate through keywords
    for word in words:
        posts = posts.filter(
            Q(title__icontains=word) | Q(post_type__iexact=word) | Q(author__iexact=word) | Q(text__icontains=word)
        ).order_by("-time")
        results["posts"] = posts
    return results


def _prepare_words(search_text):
    """strip out common words, limit to 5 words"""
    words = search_text.split()
    for common in STRIP_WORDS:
        if common in words:
            words.remove(common)
    return words[0:100]
