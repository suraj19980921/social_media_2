from django.contrib import admin
from main import models

# Register your models here.

admin.site.register([
    models.Profile,
    models.Post,
    models.Comment,
    models.Like,
    models.Friend,
    models.FriendRequest,

])