# Generated by Django 2.2.5 on 2019-10-10 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rugby', '0022_auto_20191009_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='nationality',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='rugby.Team'),
        ),
    ]
