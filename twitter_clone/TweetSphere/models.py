from django.db import models
from django.contrib.auth.models import User


# Create USer Profile

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
                                     related_name="followers",
                                     symmetrical=False,
                                     blank=True)
    
    def __str__(self):
        return self.user.username


