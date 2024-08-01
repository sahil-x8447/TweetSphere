"""
Student Name: SAHIL SHARMA
Student Number: C0930789
Course Name: Python Programming
Course Code: CSD 4523
Project Title: TWEETSPHERE -> twitter_clone
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm, SignUpForm, ProfilePicForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q

def home(request):
    """
    Handles the home page for authenticated users, allowing them to post tweets and comments.
    
    If the user is authenticated, it processes tweet and comment forms from POST requests.
    Displays all tweets and the forms for posting tweets and comments.
    """
    if request.user.is_authenticated:
        tweet_form = TweetForm(request.POST or None)
        comment_form = CommentForm(request.POST or None)
        
        if request.method == "POST":
            form_type = request.POST.get('form_type')

            if form_type == 'tweet' and tweet_form.is_valid():
                tweet = tweet_form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, "Your tweet has been posted.")
                return redirect('home')
            
            if form_type == 'comment' and comment_form.is_valid():
                tweet_id = request.POST.get('tweet_id')
                tweet = get_object_or_404(Tweet, id=tweet_id)
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.tweet = tweet
                comment.save()
                messages.success(request, "Your comment has been added.")
                return redirect('home')

        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweets": tweets, "tweet_form": tweet_form, "comment_form": comment_form})
    else:
        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweets": tweets})

def profile_list(request):
    """
    Displays a list of profiles that the current user is not following.
    
    This view requires the user to be authenticated. If not authenticated, it redirects to the home page with a message.
    """
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)  # Excluding the logged-in user's profile
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, "You must be logged in to view this page")
        return redirect('home')

def profile(request, pk):
    """
    Displays the profile of a user identified by pk.
    
    Allows the current user to follow/unfollow the displayed profile and post comments on tweets.
    """
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")
        comment_form = CommentForm(request.POST or None)

        # POST form logic
        if request.method == "POST":
            # Get current user profile
            current_user_profile = request.user.profile

            if 'follow' in request.POST:
                action = request.POST["follow"]
                # Decide to follow/unfollow
                if action == "unfollow":
                    current_user_profile.follows.remove(profile)  # Remove profile from follows list
                else:
                    current_user_profile.follows.add(profile)  # Add profile to follows list

                # Save the updated profile
                current_user_profile.save()
                return redirect('profile', pk=pk)
            
            if comment_form.is_valid():
                tweet_id = request.POST.get('tweet_id')
                tweet = get_object_or_404(Tweet, id=tweet_id)
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.tweet = tweet
                comment.save()
                messages.success(request, "Your comment has been added.")
                return redirect('profile', pk=pk)

        context = {
            'profile': profile,
            'tweets': tweets,
            'comment_form': comment_form,
        }
        return render(request, 'profile.html', context)
    else:
        messages.success(request, "You must be logged in to view this page")
        return redirect('home')

def followers(request, pk):
    """
    Displays a list of followers for the user identified by pk.
    
    Only the user themselves can view their followers. Redirects to home page if not authorized.
    """
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {"profiles": profiles})
        else:
            messages.success(request, "That's not your profile page...")
            return redirect('home')
    else:
        messages.success(request, "You must be logged in to view this page...")
        return redirect('home')

def follows(request, pk):
    """
    Displays a list of profiles that the user identified by pk is following.
    
    Only the user themselves can view their follows list. Redirects to home page if not authorized.
    """
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {"profiles": profiles})
        else:
            messages.success(request, "That's not your profile page...")
            return redirect('home')
    else:
        messages.success(request, "You must be logged in to view this page...")
        return redirect('home')

def unfollow(request, pk):
    """
    Allows the authenticated user to unfollow the profile identified by pk.
    
    Redirects to the referring page after unfollowing.
    """
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()

        messages.success(request, f"You have successfully unfollowed {profile.user.username}")
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, "You must be logged in to view this page...")
        return redirect('home')

def follow(request, pk):
    """
    Allows the authenticated user to follow the profile identified by pk.
    
    Redirects to the referring page after following.
    """
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()

        messages.success(request, f"You have successfully followed {profile.user.username}")
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, "You must be logged in to view this page...")
        return redirect('home')

def login_user(request):
    """
    Handles user login. On successful login, redirects to the home page.
    
    If login fails, redirects back to the login page with an error message.
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been successfully logged in 🥳. Start Tweeting 🦅.....")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in 😱. Please try again.......")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    """
    Logs out the user and redirects to the home page with a success message.
    """
    logout(request)
    messages.success(request, "You have been successfully logged out.....")
    return redirect('home')

def register_user(request):
    """
    Handles user registration. On successful registration, logs in the user and redirects to the home page.
    
    Displays a registration form and processes form submission.
    """
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Login the newly registered user
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered! Welcome!")
            return redirect('home')

    return render(request, 'register.html', {'form': form})

def update_user(request):
    """
    Allows the authenticated user to update their profile and account details.
    
    Displays forms for updating user information and profile picture.
    """
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        
        # Get forms for updating user and profile
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            login(request, current_user)
            messages.success(request, "Your profile has been updated!")
            return redirect('home')

        return render(request, "update_user.html", {'user_form': user_form, 'profile_form': profile_form})
    else:
        messages.success(request, "You must be logged in to view that page...")
        return redirect('home')

def tweet_like(request, pk):
    """
    Allows the authenticated user to like or unlike a tweet identified by pk.
    
    Toggles the like status and redirects to the referring page.
    """
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, "You must be logged in to like a tweet...")
        return redirect('home')

def tweet_show(request, pk):
    """
    Displays a specific tweet identified by pk.
    
    Shows the tweet details and redirects with a message if the tweet does not exist.
    """
    tweet = get_object_or_404(Tweet, id=pk)
    if tweet:
        return render(request, 'show_tweet.html', {'tweet': tweet})
    else:
        messages.success(request, "Your tweet does not exist...")
        return redirect('home')

def delete_tweet(request, pk):
    """
    Allows the authenticated user to delete a tweet they own.
    
    Redirects to the referring page with a success or error message based on ownership.
    """
    if request.user.is_authenticated:
        tweet_instance = get_object_or_404(Tweet, id=pk)
        # Check ownership of the tweet
        if request.user.username == tweet_instance.user.username:
            tweet_instance.delete()
            messages.success(request, "The tweet has been deleted!")
            return redirect(request.META.get("HTTP_REFERER"))    
        else:
            messages.success(request, "You don't own that tweet!!")
            return redirect('home')

    else:
        messages.success(request, "Please log in to continue...")
        return redirect(request.META.get("HTTP_REFERER"))

def edit_tweet(request, pk):
    """
    Allows the authenticated user to edit a tweet they own.
    
    Displays the tweet form and updates the tweet if the form is valid.
    """
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)

        # Check ownership of the tweet
        if request.user.username == tweet.user.username:
            
            form = TweetForm(request.POST or None, instance=tweet)
            if request.method == "POST":
                if form.is_valid():
                    tweet = form.save(commit=False)
                    tweet.user = request.user
                    tweet.save()
                    messages.success(request, "Your tweet has been updated!")
                    return redirect('home')
            else:
                return render(request, "edit_tweet.html", {'form': form, 'tweet': tweet})
        
        else:
            messages.success(request, "You don't own that tweet!!")
            return redirect('home')

    else:
        messages.success(request, "Please log in to continue...")
        return redirect('home')

def search_users(request):
    """
    Searches for users based on a query.
    
    Displays users whose username or name matches the query.
    """
    query = request.GET.get('query')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        ).select_related('profile')
    else:
        users = User.objects.none()
    return render(request, 'search_results.html', {'users': users, 'query': query})
