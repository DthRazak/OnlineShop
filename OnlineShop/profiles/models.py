from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, unique=False, db_index=True, verbose_name="First name")
    last_name = models.CharField(max_length=30, unique=False, db_index=True, verbose_name="Last name")
    subscribe = models.BooleanField(default=False, verbose_name="Subscribe")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()