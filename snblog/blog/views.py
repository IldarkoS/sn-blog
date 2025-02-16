from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils import timezone

from .models import Post, Category

def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )[1:6]
    context = {
        "post_list": post_list
    }
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post,
        pk=pk,
        pub_date__lte=timezone.now(),
    )
    context = {
        "post": post
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug = category_slug,
        is_published=True
    )
    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now(),
        )
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)