# Generated by Django 2.2.4 on 2019-08-12 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rugby', '0010_auto_20190812_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(default=79, on_delete=django.db.models.deletion.CASCADE, to='rugby.Team'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='try',
            name='team',
            field=models.ForeignKey(default=79, on_delete=django.db.models.deletion.CASCADE, to='rugby.Team'),
            preserve_default=False,
        ),
    ]