from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Followers


def index(request):
    # handle user post submission
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        content = request.POST["content"]
        if content:
            post = Post(user=request.user, content=content)
            post.save()
        return HttpResponseRedirect(reverse("index"))
    
    # display all posts
    posts = Post.objects.all().order_by("-timestamp").all()
    return render(request, "network/index.html", {
        "posts": posts
    })


# user profile view
def profile_view(request, username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    user = User.objects.get(username=username)
    followers_count = user.followers.count()
    following_count = user.following.count()

    # if user follows then buttion will be unfollow else follow
    is_following = Followers.objects.filter(user=user, follower=request.user).exists()
   
    return render(request, "network/profile_view.html", {
        "profile_user": user,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following
    })

def follow(request, username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    user_to_follow = User.objects.get(username=username)
    if user_to_follow == request.user:
        return HttpResponseRedirect(reverse("profile", args=[username]))
    
    # Check if already following
    existing_follow = Followers.objects.filter(user=user_to_follow, follower=request.user).first()
    if existing_follow:
        # Unfollow
        existing_follow.delete()
    else:
        # Follow
        new_follow = Followers(user=user_to_follow, follower=request.user)
        new_follow.save()
    
    return HttpResponseRedirect(reverse("profile", args=[username]))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
