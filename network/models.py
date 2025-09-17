from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}..."
    
    @property
    def like_count(self):
        return self.likes.count()
    

class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    number_of_followers = models.IntegerField(default=0)
    number_of_following = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'follower')
    

    def __str__(self):
        return f"{self.follower.username} follows {self.user.username}"
    
    
class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    

    class Meta:
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f"{self.user.username} liked post {self.post.id}"