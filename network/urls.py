
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>", views.profile_view, name="profile"),
    path("explore", views.explore, name="explore"),
    path("follow/<str:username>/", views.follow, name="follow"),
    path("post/<int:post_id>/like/", views.toggle_like, name="toggle-like"),
    path("edit-post/<int:post_id>/", views.edit_post_content, name="edit-post"),
    path("edit-post", views.edit_post_content, name="edit-post"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
