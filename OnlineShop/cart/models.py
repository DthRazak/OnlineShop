from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from profiles.models import Profile
from goods.models import Good


class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    total = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True, verbose_name="Is active")

    def __str__(self):
        return "Cart - " + self.profile.user.username


class CartItem(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    material = models.CharField(max_length=10, default='rubber', verbose_name="Material")

    def __str__(self):
        return self.cart.profile.user.username + " - " + self.good.name


@receiver(pre_save, sender=CartItem)
def update_cart_total(sender, instance, **kwargs):
    if not instance._state.adding:
        db_instace = CartItem.objects.filter(cart=instance.cart, good=instance.good)[0]
        if db_instace.good.price_acc is None or db_instace.good.price >= db_instace.good.price:
            prev_cost = db_instace.quantity * db_instace.good.price
        else:
            prev_cost = db_instace.quantity * db_instace.good.price_acc
    else:
        prev_cost = 0.0

    if instance.good.price_acc is None or instance.good.price >= instance.good.price:
        cost = instance.quantity * instance.good.price
    else:
        cost = instance.quantity * instance.good.price_acc
    instance.cart.total -= prev_cost
    instance.cart.total += cost
    instance.cart.save()
