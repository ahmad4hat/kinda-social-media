from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Room(models.Model):
    room_type = models.CharField(default="oto", max_length=50)


class RoomUser(models.Model):
    user = models.ForeignKey(get_user_model(),  on_delete=models.CASCADE)
    room_user = models.ForeignKey(
        Room, related_name='room_users', on_delete=models.CASCADE)
