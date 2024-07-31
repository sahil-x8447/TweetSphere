from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save # when  saving in database it gives signal or notification u can say  


# Tweet model
class Tweet(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='tweets') # related_name
    body = models.CharField(max_length=200) # tweets max length
    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add=True means when we create
    likes = models.ManyToManyField(User, related_name="tweet_like", blank=True)
    
    # Keep track of number of likes
    def number_of_likes(self):
        return self.likes.count()
 
    
    def __str__(self):
        return(
            f"({self.user}) "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body}..."
        )

# Create USer Profile

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
                                     related_name="followed_by",
                                     symmetrical=False,
                                     blank=True)
    
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(null=True,blank=True, upload_to="images/")
    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    facebook_link = models.CharField(null=True, blank=True, max_length=100)
    instagram_link = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.user.username



# Create profile when new user sign up

def create_profile(sender ,instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance) # whatever is the user it will go to instance
        user_profile.save() # saving 
        # user follows themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save() # saving 


post_save.connect(create_profile, sender=User)


