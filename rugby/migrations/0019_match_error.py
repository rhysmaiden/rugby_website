# Generated by Django 2.2.5 on 2019-10-09 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rugby', '0018_match_video_downloaded'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='error',
            field=models.IntegerField(default=0),
        ),
    ]