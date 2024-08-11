
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('newPost', views.new_post, name="post"),
    path('profile/<int:user_id>', views.view_profile, name="users_profile"),
    path('follow/<int:id>', views.follow_user, name="follow_user"),
    path('unfollow/<int:id>', views.unfollow_user, name="unfollow_user"),
    path('followingPost', views.following_post, name='following_post'),
    path('likePost/<int:post_id>', views.like_post, name='like'),
    path('unlikePost/<int:post_id>', views.unlike_post, name="unlike"),
    path('is_liked/<int:post_id>', views.is_liked, name="is_liked"),
    path('is_follow/<int:user_id>', views.is_follow, name="is_follow"),
    path('edit_post/<int:post_id>', views.edit_post, name="edit_post" )
]
