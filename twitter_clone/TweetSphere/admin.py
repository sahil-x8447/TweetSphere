from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile

# Unregister the Group model from the admin site
admin.site.unregister(Group)

# Combining Profile and user into Section

class ProfileInline(admin.StackedInline):
    model = Profile



# Extend our User Model

class UserAdmin(admin.ModelAdmin):
    model = User
    # Display username only
    fields = ["username"]
    inlines = [ProfileInline]

# unregistering the intial User
admin.site.unregister(User)

# Reregister User
admin.site.register(User, UserAdmin)

# Register Profile

#admin.site.register(Profile)




