from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now


# Create your models here.
class Item (models.Model):
    type = models.CharField(max_length=30,default="post")
    by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=now)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    deactivate = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)


class Like (models.Model):
    user = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.CASCADE)
    track = models.ForeignKey(
        Item, related_name='likes', on_delete=models.CASCADE)
