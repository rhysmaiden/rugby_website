# Generated by Django 2.2.4 on 2019-08-12 04:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rugby', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='league',
        ),
        migrations.RemoveField(
            model_name='team',
            name='league',
        ),
    ]
