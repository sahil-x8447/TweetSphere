"""
Student Name: SAHIL SHARMA
Student Number: C0930789
Course Name: Python Programming
Course Code: CSD 4523
Project Title: TWEETSPHERE -> twitter_clone
"""

from django import forms
from .models import Tweet, Profile, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Form for updating the user profile
class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture", required=False)
    profile_bio = forms.CharField(
        label="", 
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Profile Bio'}),
        required=False
    )
    facebook_link = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Facebook Link'}),
        required=False
    )
    instagram_link = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instagram Link'}),
        required=False
    )

    class Meta:
        model = Profile
        fields = ('profile_image', 'profile_bio', 'facebook_link', 'instagram_link')

# Form for creating or editing tweets
class TweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "What's happening!",
                "class": "form-control",
            }
        ),
        label="",
    )
    
    class Meta:
        model = Tweet
        exclude = ("user", "likes")  # Exclude user and likes fields from the form

# Form for user registration
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="", 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'})
    )
    first_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'})
    )
    last_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and customize widget attributes.
        """
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        # Store the initial username if an instance is provided
        if self.instance:
            self.initial_username = self.instance.username
        else:
            self.initial_username = None

        # Customize widget attributes for username field
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<span class="form-text text-muted">'
            '<small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small>'
            '</span>'
        )

        # Customize widget attributes for password1 field
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Your password can\'t be too similar to your other personal information.</li>'
            '<li>Your password must contain at least 8 characters.</li>'
            '<li>Your password can\'t be a commonly used password.</li>'
            '<li>Your password can\'t be entirely numeric.</li>'
            '</ul>'
        )

        # Customize widget attributes for password2 field
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = (
            '<span class="form-text text-muted">'
            '<small>Enter the same password as before, for verification.</small>'
            '</span>'
        )

    def clean_username(self):
        """
        Validate that the username is unique.
        """
        username = self.cleaned_data.get('username')
        
        # Only perform the unique check if the username has changed
        if self.initial_username and self.initial_username == username:
            return username
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

# Form for searching users
class UserSearchForm(forms.Form):
    query = forms.CharField(label='Search Users', max_length=100)

# Form for creating or editing comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
