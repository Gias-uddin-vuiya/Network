from django.contrib import admin

# Register your models here.
from .models import User, Post, Followers, Like_and_unlike

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Followers)
admin.site.register(Like_and_unlike)


