from django import template
from services.models import Page, Post
from django.core.paginator import Paginator

register = template.Library()


@register.inclusion_tag('services/pages_tpl.html', takes_context=True)
def show_pages(context):
    path = context['request'].path
    pages = Page.objects.all()
    return {'path': path, 'pages': pages}


@register.simple_tag(takes_context=True)
def show_posts(context):
    posts = Post.objects.all()
    paginator = Paginator(posts, 2)
    page_number = context['request'].GET.get('page')
    return paginator.get_page(page_number)

@register.simple_tag
def show_first_post():
    return Post.objects.first()
