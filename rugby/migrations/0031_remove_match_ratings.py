# Generated by Django 2.2.4 on 2019-11-05 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rugby', '0030_auto_20191105_0814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='ratings',
        ),
    ]