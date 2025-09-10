from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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
    paginator = Paginator(posts, 4)  # Show 10 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": posts,
    })


# user profile view
def profile_view(request, username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    user = User.objects.get(username=username)
    # count followers and following
    followers_count = user.followers.count()
    following_count = user.following.count()
    # add pagination
    post = user.posts.all().order_by("-timestamp") # reverse chronological order
    paginator = Paginator(post, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    # if user follows then buttion will be unfollow else follow
    is_following = Followers.objects.filter(user=user, follower=request.user).exists()
   
    return render(request, "network/profile_view.html", {
        "profile_user": user,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
        "page_obj": page_obj
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

# following page
def following(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    # get users that the current user is following
    following_users = Followers.objects.filter(follower=request.user).values_list('user', flat=True)
    posts = Post.objects.filter(user__in=following_users).order_by('-timestamp')
    
    return render(request, "network/following.html", {
        "posts": posts
    })

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
