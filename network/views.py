from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect 
from django.urls import reverse


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

from .models import User, Post, Followers, Reaction


def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Reaction.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
    
    
    return JsonResponse({
        "likes": post.like_count,
        "liked": created  # True if just liked, False if unliked
    })

def edit_post_content(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id, user=request.user)
        new_content = request.POST.get("content")

        if not new_content:
            return JsonResponse({"success": False, "error": "Content is required"})

        post.content = new_content
        post.save()

        return JsonResponse({"success": True, "updated_content": post.content})

    return JsonResponse({"success": False, "error": "Invalid request"})

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
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # post liked by users
    if request.user.is_authenticated:
        for post in posts:
            post.liked_by_user = post.likes.filter(user=request.user).exists()
    else:
        for post in posts:
            post.liked_by_user = False
    

    return render(request, "network/index.html", {
        "posts": posts,
    })

# explore page
def explore(request):
    return render(request, "network/explore.html")

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

     # post liked by users
    if request.user.is_authenticated:
        for post in posts:
            post.liked_by_user = post.likes.filter(user=request.user).exists()
    else:
        for post in posts:
            post.liked_by_user = False
    
    
    return render(request, "network/following.html", {
        "posts": posts
    })

def following_users(request, username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    profile_user = get_object_or_404(User, username=username)
    # get users that the current user is following
    user_followings = Followers.objects.filter(follower=profile_user).values_list('user', flat=True)
    followed_users = User.objects.filter(id__in=user_followings)

    
    return render(request, "network/user_following.html", {
        "profile_user": profile_user,
        "followed_users": followed_users,
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
