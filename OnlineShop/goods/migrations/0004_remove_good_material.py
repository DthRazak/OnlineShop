# Generated by Django 2.2.7 on 2019-12-15 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20191215_1455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='good',
            name='material',
        ),
    ]
