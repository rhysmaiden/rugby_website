# Generated by Django 2.2.4 on 2019-08-16 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rugby', '0017_auto_20190815_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='video_downloaded',
            field=models.IntegerField(default=0),
        ),
    ]
