# Generated by Django 2.2.4 on 2019-08-12 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rugby', '0011_auto_20190812_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='team',
        ),
        migrations.RemoveField(
            model_name='try',
            name='team',
        ),
    ]
