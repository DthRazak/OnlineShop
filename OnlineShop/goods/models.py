from django.db import models
from categories.models import Category
from django.urls import reverse


class Good(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True, verbose_name="Name")
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Short description")
    content = models.TextField(verbose_name="Additional information")
    price = models.FloatField(db_index=True, verbose_name="Price")
    price_acc = models.FloatField(null=True, blank=True, verbose_name="Price with discount")
    in_stock = models.BooleanField(default=True, db_index=True, verbose_name="In stock")
    featured = models.BooleanField(default=False, db_index=True, verbose_name="Recommended")
    image = models.ImageField(upload_to="goods/list", verbose_name="Main image")

    def save(self, *args, **kwargs):
        try:
            this_record = Good.objects.get(pk=self.pk)
            if this_record.image != self.image:
                this_record.image.delete(save=False)
        except:
            pass
        super(Good, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(Good, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("goods_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Good"
        verbose_name_plural = "Goods"


class GoodImage(models.Model):
    good = models.ForeignKey(Good, verbose_name="Good", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="goods/detail", verbose_name="Additional image")

    def save(self, *args, **kwargs):
        try:
            this_record = GoodImage.objects.get(pk=self.pk)
            if this_record.image != self.image:
                this_record.image.delete(save=False)
        except:
            pass
        super(GoodImage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(GoodImage, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Good image"
        verbose_name_plural = "Good images"
