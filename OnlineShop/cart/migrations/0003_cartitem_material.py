# Generated by Django 2.2.7 on 2019-12-15 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20191215_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='material',
            field=models.CharField(default='rubber', max_length=10, verbose_name='Material'),
        ),
    ]
