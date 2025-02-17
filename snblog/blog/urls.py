from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('posts/create/', views.CreatePostView.as_view(), name='create_post'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', views.UpdatePostView.as_view(), name='edit_post'),
    path('posts/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('posts/<int:post_id>/comment/', views.CreateCommentView.as_view(), name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:pk>/', views.UpdateCommentView.as_view(), name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:pk>/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),
    path('profile/edit/', views.update_user_profile, name='edit_profile'),
    path('profile/<slug:username>/', views.user_profile, name='profile'),
]
