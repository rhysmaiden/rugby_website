# Generated by Django 2.2.5 on 2019-10-11 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rugby', '0027_team_league_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='league_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='rugby.League'),
        ),
    ]