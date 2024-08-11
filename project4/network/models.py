from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

   


class New_post(models.Model):
    # Create the field for the user, content, posted_at
    poster = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="post_by_user")
    content = models.CharField(max_length=200)
    posted_at = models.DateTimeField(blank=True)
    #Create the field for the Likes put it for pending
    likes = models.ManyToManyField(User, blank=True, related_name="likes_on_a_post", null=True)    
    likes_count = models.IntegerField(default=0, blank=True)
    
    def __str__(self):
        return f"User:{self.poster} Posted_at:{self.posted_at} Content:{self.content} ID: {self.id}"
    
   
    def serialize(self):
        return {
            "post_id": self.id,
            "content": self.content,
            "poster": self.poster.username,
            'user_id': self.poster.id,
            'posted_at': self.posted_at
        }

    
class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="who_follow_users" )
    followers = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="followers")
    
    def __str__(self):
        return f"User: {self.user} Follower: {self.followers}"
    
class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="whom_user_is_following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='following')
    
    def __str__(self):
        return f"User: {self.user} Following: {self.following}"