"""
Student Name: SAHIL SHARMA
Student Number: C0930789
Course Name: Python Programming
Course Code: CSD 4523
Project Title: TWEETSPHERE -> twitter_clone
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Tweet model
class Tweet(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.DO_NOTHING, 
        related_name='tweets'
    )  # related_name allows us to access user's tweets with user.tweets
    body = models.CharField(max_length=200)  # Maximum length for a tweet
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set creation time
    likes = models.ManyToManyField(User, related_name="tweet_like", blank=True)  # Users who liked the tweet
    
    def number_of_likes(self):
        """
        Returns the number of likes for the tweet.
        """
        return self.likes.count()
    
    def __str__(self):
        """
        Returns a string representation of the Tweet.
        """
        return (
            f"({self.user}) "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body}..."
        )

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,  # Relationship is not symmetrical (user A can follow user B without B following A)
        blank=True
    )
    date_modified = models.DateTimeField(auto_now=True)  # Automatically set to the current time when modified
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")  # Profile picture
    profile_bio = models.CharField(null=True, blank=True, max_length=500)  # User biography
    facebook_link = models.CharField(null=True, blank=True, max_length=100)  # Facebook profile link
    instagram_link = models.CharField(null=True, blank=True, max_length=100)  # Instagram profile link

    def __str__(self):
        """
        Returns a string representation of the Profile.
        """
        return self.user.username

# Signal to create a Profile when a new User is created
def create_profile(sender, instance, created, **kwargs):
    """
    Creates a Profile for a newly created User and sets up self-following.
    """
    if created:
        user_profile = Profile(user=instance)  # Create Profile with the new User
        user_profile.save()  # Save Profile to the database
        user_profile.follows.set([instance.profile.id])  # Set user to follow themselves
        user_profile.save()  # Save Profile to the database

# Connect the create_profile function to the post_save signal for the User model
post_save.connect(create_profile, sender=User)

# Comment model
class Comment(models.Model):
    tweet = models.ForeignKey(
        Tweet, 
        related_name='comments', 
        on_delete=models.CASCADE
    )  # Reference to the Tweet the comment is associated with
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )  # User who made the comment
    body = models.TextField()  # Content of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set creation time
