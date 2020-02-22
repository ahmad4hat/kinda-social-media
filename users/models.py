from django.contrib.auth import get_user_model
from django.db import models


class Friend(models.Model):
    user = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.DO_NOTHING)
    friend = models.ForeignKey(
        get_user_model(), null=True, related_name='friends', on_delete=models.DO_NOTHING)


# class model()
