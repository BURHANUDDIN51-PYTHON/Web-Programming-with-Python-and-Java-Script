from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import User, New_post, Followers, Following
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json



def index(request):
    # rendering all the post from all the users with the help of Javascipt
    posts  = New_post.objects.order_by('posted_at').reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    current_user = request.user
    return render(request, "network/index.html", {
        'posts': page_obj,    
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


def new_post(request):
    # getting the data and inserting it into the tables
    content = request.POST['content']
    if not content:
        return HttpResponseRedirect(reverse('index'))
    current_user = request.user
    post = New_post(content=content,poster=current_user,posted_at=datetime.now())
    post.save()
    return HttpResponseRedirect(reverse('index'))


def all_posts(request):
    # Getting all the post from the New_posts model
    posts  = New_post.objects.order_by('posted_at').reverse()
    return HttpResponse(posts)

@login_required
def view_profile(request, user_id):
    # Get all the post which are related to that user 
    user_instance = User.objects.filter(pk=user_id).first()
    user_posts = user_instance.post_by_user.all()
    
    # Pagination process
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculating the followers and followings of the user_instance
    followers = user_instance.who_follow_users.all()
    following = user_instance.whom_user_is_following.all()
    
    
    # Finding out whether the current user follows the user_instance or not 
    is_follow = False
    current_user = request.user
    for each_following in current_user.whom_user_is_following.all():
        if user_instance == each_following.following:
            is_follow = True
            break
   
    return render(request, 'network/profile.html', {
        'posts_count': len(user_posts),
        "posts": page_obj,
        "user":user_instance,
        "btn": True if user_instance != request.user else False,
        "followers": len(followers),
        "following": len(following),
        'is_follow': is_follow,
        })

def unfollow_user(request,id):
    try:
        # Get the current user and the user whom to be unfollowed
        current_user = request.user
        user = User.objects.get(pk=id)
        
        
        # Doing the two step process of unfollowing the user and also removing the current user from it's followers
        following_instance = Following.objects.filter(user=current_user, following=user)
        followers_instance = Followers.objects.filter(user=user, followers=current_user)
        followers_instance.delete()
        following_instance.delete()
        
        
        # Passing the followers count
        followers_count = len(Followers.objects.filter(user=user).all())
        return JsonResponse({'followers': followers_count})
     
    except:
        return JsonResponse({'error':"Row has not been deleted properly"})
    
def follow_user(request, id):
    try:
        # Get the current user and the user whom to be unfollowed
        current_user = request.user
        user = User.objects.get(pk=id)
        
        
        # Doing the two step process of unfollowing the user and also removing the current user from it's followers
        following_instance = Following(user=current_user, following=user)
        followers_instance = Followers(user=user, followers=current_user)
        followers_instance.save()
        following_instance.save()
        
        
        # Passing the followers count
        followers_count = len(Followers.objects.filter(user=user).all())
        return JsonResponse({'followers': followers_count})
    except:
        return JsonResponse({'error':"Row has not been added properly"})


def following_post(request):
    # Getting the current user and it's following list
    current_user = request.user
    user_follows = Following.objects.filter(user=current_user).all()
    
    
    # Getting the posts of the users whom the current user follows
    posts = []
    for each_user_follows in user_follows:
        user = each_user_follows.following
        posts += user.post_by_user.all()  
        
    # Pagination Process
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
         
    return render(request, "network/index.html", {
        'posts': page_obj,        
        })
    
    
def like_post(request,post_id):
    if request.method == 'GET':
        post = New_post.objects.get(pk=post_id)
        current_user = request.user
        post.likes.add(current_user)
        post.likes_count += 1
        post.save()
        return JsonResponse({"likes": len(post.likes.all()), 'is_liked': True}, status=200)
    
def unlike_post(request, post_id):
    if request.method == "GET":
        post = New_post.objects.get(pk=post_id)
        current_user = request.user
        post.likes.remove(current_user)
        post.likes_count -= 1
        post.save()
        return JsonResponse({"likes": len(post.likes.all()), "is_liked": False}, status=200)

    
def is_liked(request, post_id):
    post = New_post.objects.get(pk=post_id)
    current_user = request.user
    if current_user in post.likes.all():
        return JsonResponse({'is_liked': True})
    return JsonResponse({"is_liked": False})
    
    
def is_follow(request, user_id):
    if request.method == "GET":
        user_follows = False
        user_instance = User.objects.get(pk=user_id)
        current_user = request.user
        for each_following in current_user.whom_user_is_following.all():
            if user_instance == each_following.following:
                user_follows = True
                break
        return JsonResponse({'is_follow': user_follows})
    


@login_required
def edit_post(request, post_id):
    if request.method == "PUT":
        # Load the request body
        data = json.loads(request.body)
        content = data.get('content')
        if content is not None:
            post = New_post.objects.get(pk=post_id)
            post.content = content
            post.save()
        return JsonResponse({'content': content}, status=200)