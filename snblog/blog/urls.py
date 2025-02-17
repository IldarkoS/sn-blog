from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('posts/create/', views.CreatePostView.as_view(), name='create_post'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', views.UpdatePostView.as_view(), name='edit_post'),
    path('posts/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),
    path('profile/edit/', views.update_user_profile, name='edit_profile'),
    path('profile/<slug:username>/', views.user_profile, name='profile'),
]