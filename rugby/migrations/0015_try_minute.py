# Generated by Django 2.2.4 on 2019-08-15 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rugby', '0014_auto_20190815_0431'),
    ]

    operations = [
        migrations.AddField(
            model_name='try',
            name='minute',
            field=models.IntegerField(default=0),
        ),
    ]
