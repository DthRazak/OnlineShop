from django.contrib.auth.models import User
from django.db import models

from goods.models import Good


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text = models.TextField(max_length=1000, verbose_name="Text")
    good = models.ForeignKey(Good, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}. {1}: {2}".format(self.id, self.user.username, self.good.name)
