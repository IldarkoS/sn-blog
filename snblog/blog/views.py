from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponseRedirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Post, Category, User
from .forms import UserEditForm

class PostListView(ListView):
    model = Post
    ordering = ('id',)
    paginate_by = 10
    queryset = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).select_related('author').select_related('category').select_related('location')
    template_name = 'blog/index.html'


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related('author').select_related('category').select_related('location'),
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
    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now(),
        ).select_related('author').select_related('category').select_related('location')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj
    }
    return render(request, template, context)


def user_profile(request, username):
    profile = get_object_or_404(
        User,
        username=username
    )
    posts = Post.objects.filter(author=profile).select_related('category').select_related('location').select_related('author')
    template = 'blog/profile.html'

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'page_obj': page_obj
    }
    return render(request, template, context)


@login_required
def update_user_profile(request):
    template = 'blog/user.html'
    instance = get_object_or_404(User, pk=request.user.id)
    form = UserEditForm(
        request.POST or None,
        instance=instance
    )
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect(f'/profile/{form.instance.username}')
    return render(request, template, context)