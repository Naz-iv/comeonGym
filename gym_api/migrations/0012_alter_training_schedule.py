# Generated by Django 5.0.3 on 2024-03-07 10:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gym_api", "0011_alter_training_schedule"),
    ]

    operations = [
        migrations.AlterField(
            model_name="training",
            name="schedule",
            field=models.ForeignKey(
                default=11,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="trainings",
                to="gym_api.schedule",
            ),
            preserve_default=False,
        ),
    ]
