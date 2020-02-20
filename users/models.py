from django.contrib.auth import get_user_model
from django.db import models


class Friend(models.Model):
    user = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.CASCADE)
    friend = models.ForeignKey(
        get_user_model(), related_name='friends', on_delete=models.CASCADE)


# class model()
