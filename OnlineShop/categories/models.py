from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, db_index=True, unique=True, verbose_name="Name")
    order = models.PositiveSmallIntegerField(default=0, db_index=True, verbose_name="Sequence number")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'categories'
        ordering = ['order']
