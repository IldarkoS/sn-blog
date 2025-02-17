from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),
    path('profile/edit/', views.update_user_profile, name='edit_profile'),
    path('profile/<slug:username>/', views.user_profile, name='profile'),
]