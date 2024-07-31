from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q




def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method=="POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, ("Your tweet has been Posted"))
                return redirect('home')



        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request,'home.html', {"tweets":tweets, "form":form})
    else:
        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request,'home.html', {"tweets":tweets})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user) # excluding the user whose logged in
        return render(request,'profile_list.html', {"profiles":profiles})
    else:
        messages.success(request, ("You must be Logged in to view this page"))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")


        # POST form logic
        if request.method == "POST": #this means user clicked the button
            # Get current user
            current_user_profile = request.user.profile

            action = request.POST["follow"]
            # decide to follow/unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile) # remove the profile from the current user's follows list
            else:
                current_user_profile.follows.add(profile) # add the profile to the current user's follows list

            # save profile
            current_user_profile.save()




        return render(request,'profile.html', {"profile":profile, "tweets":tweets})
    else:
        messages.success(request, ("You must be Logged in to view this page"))
        return redirect('home')
    
def followers(request, pk):
	if request.user.is_authenticated:
		if request.user.id == pk:
			profiles = Profile.objects.get(user_id=pk)
			return render(request, 'followers.html', {"profiles":profiles})
		else:
			messages.success(request, ("That's Not Your Profile Page..."))
			return redirect('home')	
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')
     

def follows(request, pk):
	if request.user.is_authenticated:
		if request.user.id == pk:
			profiles = Profile.objects.get(user_id=pk)
			return render(request, 'follows.html', {"profiles":profiles})
		else:
			messages.success(request, ("That's Not Your Profile Page..."))
			return redirect('home')	
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')


def unfollow(request, pk):
	if request.user.is_authenticated:
		# Get the profile to unfollow
		profile = Profile.objects.get(user_id=pk)
		# Unfollow the user
		request.user.profile.follows.remove(profile)
		# Save our profile
		request.user.profile.save()

		# Return message
		messages.success(request, (f"You Have Successfully Unfollowed {profile.user.username}"))
		return redirect(request.META.get("HTTP_REFERER"))

	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')
    
def follow(request, pk):
	if request.user.is_authenticated:
		# Get the profile to unfollow
		profile = Profile.objects.get(user_id=pk)
		# Unfollow the user
		request.user.profile.follows.add(profile)
		# Save our profile
		request.user.profile.save()

		# Return message
		messages.success(request, (f"You Have Successfully Followed {profile.user.username}"))
		return redirect(request.META.get("HTTP_REFERER"))

	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, ("You have been  successfully logged in 🥳. Start Tweeting 🦅....."))
            return redirect('home')
        else:
            messages.success(request, ("There was a error logging in 😱. Please Try Again......."))
            return redirect('login')
    else:
        return render(request,'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been successfully logged out....."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Login
            user = authenticate(request, username=username, password=password)
            login(request,user)
            messages.success(request, ("You have successfully registered! Welcome!"))
            return redirect('home')


    return render(request,'register.html', {'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        
        # Get Forms
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            login(request, current_user)
            messages.success(request, "Your Profile Has Been Updated!")
            return redirect('home')

        return render(request, "update_user.html", {'user_form': user_form, 'profile_form': profile_form})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')
    

def tweet_like(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
            
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, "You Must Be Logged In To Like A Tweet...")
        return redirect('home')


def tweet_show(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    if tweet:
        return render(request, 'show_tweet.html', {'tweet': tweet})
    else:
        messages.success(request, "You tweet does not exist...")
        return redirect('home')
    

def delete_tweet(request, pk):
    if request.user.is_authenticated:
        tweet_instance = get_object_or_404(Tweet, id=pk)
        # Check to see if you own the tweet
        if request.user.username == tweet_instance.user.username:
            # Delete The tweet
            tweet_instance.delete()
            
            messages.success(request, ("The tweet Has Been Deleted!"))
            return redirect(request.META.get("HTTP_REFERER"))    
        else:
            messages.success(request, ("You Don't Own That tweet!!"))
            return redirect('home')

    else:
        messages.success(request, ("Please Log In To Continue..."))
        return redirect(request.META.get("HTTP_REFERER"))

def edit_tweet(request,pk):
	if request.user.is_authenticated:
		# Grab The tweet!
		tweet = get_object_or_404(Tweet, id=pk)

		# Check to see if you own the tweet
		if request.user.username == tweet.user.username:
			
			form = TweetForm(request.POST or None, instance=tweet)
			if request.method == "POST":
				if form.is_valid():
					tweet = form.save(commit=False)
					tweet.user = request.user
					tweet.save()
					messages.success(request, ("Your tweet Has Been Updated!"))
					return redirect('home')
			else:
				return render(request, "edit_tweet.html", {'form':form, 'tweet':tweet})
	
		else:
			messages.success(request, ("You Don't Own That tweet!!"))
			return redirect('home')

	else:
		messages.success(request, ("Please Log In To Continue..."))
		return redirect('home')

     



def search_users(request):
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
