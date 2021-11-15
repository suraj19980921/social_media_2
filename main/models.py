from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import ModelState
from django.db.models.fields import DateField

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    online = models.BooleanField(default=False)
   
    
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.TextField()
    image = models.ImageField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

class Friend(models.Model):
    personOne = models.ForeignKey(User,on_delete=models.CASCADE, related_name="personOne")
    personTwo = models.ForeignKey(User,on_delete=models.CASCADE, related_name = "personTwo")

class FriendRequest(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE, related_name = "receiver")
