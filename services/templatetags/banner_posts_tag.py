from django import template
from services.models import Post

register = template.Library()

@register.simple_tag
def show_banner_posts():
    posts = Post.objects.filter(banner_published=True)
    for post in posts:
        post.content = post.content[:post.content.find('<div class="LTRStyle"')]
    return posts
