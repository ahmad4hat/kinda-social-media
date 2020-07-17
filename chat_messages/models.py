# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model as user
from django.utils.timezone import now
from django.db import models
from rooms.models import Room

# Create your models here.


class ChatMessage(models.Model):
    text = models.TextField()
    by = models.ForeignKey(user(), on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=now)
