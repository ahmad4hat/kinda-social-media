from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model as user
from django.utils.timezone import now

# Create your models here.


class ChatMessage(models.Model):
    text = models.TextField()
    by = models.ForeignKey(user(), on_delete=models.CASCADE)
    # room needs to be added
