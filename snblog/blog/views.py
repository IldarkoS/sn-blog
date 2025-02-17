from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponseRedirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.db.models import Count

from .models import Post, Category, User, Comment
from .forms import UserEditForm, CreatePostForm, CommentForm


class PostMixin:
    model = Post


class PostListView(ListView, PostMixin):
    ordering = ('id',)
    paginate_by = 10
    queryset = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).select_related('author').select_related('category').select_related('location'
    ).annotate(comment_count=Count('comments'))
    template_name = 'blog/index.html'


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related('author').select_related('category').select_related('location'),
        pk=pk,
    )
    comments = Comment.objects.filter(post=post).select_related('author')
    form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': comments,
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
        return redirect(f'/profile/{form.instance.username}/')
    return render(request, template, context)


class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'blog/create.html'
    form_class = CreatePostForm


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user.username})


class UpdatePostView(LoginRequiredMixin, PostMixin, UpdateView):
    template_name = 'blog/create.html'
    form_class = CreatePostForm

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DeletePostView(LoginRequiredMixin, PostMixin, DeleteView):
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user.username})

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CommentMixin:
    model = Comment


class CreateCommentView(LoginRequiredMixin, CommentMixin, CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['post_id']})

class UpdateCommentView(LoginRequiredMixin, CommentMixin, UpdateView):
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, pk=kwargs['pk'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DeleteCommentView(LoginRequiredMixin, CommentMixin, DeleteView):
    template_name = 'blog/comment.html'

    def get_success_url(self):
        comment = self.get_object()
        return reverse('blog:post_detail', kwargs={'pk': comment.post.id})

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, pk=kwargs['pk'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)