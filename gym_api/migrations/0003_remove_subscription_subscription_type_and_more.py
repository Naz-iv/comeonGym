# Generated by Django 5.0.3 on 2024-03-05 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gym_api", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscription",
            name="subscription_type",
        ),
        migrations.AddField(
            model_name="subscription",
            name="number_of_workouts",
            field=models.IntegerField(
                choices=[(1, 1), (4, 4), (8, 8), (12, 12)], default=1
            ),
        ),
        migrations.AddField(
            model_name="subscription",
            name="price",
            field=models.IntegerField(default=280),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="subscription",
            name="sub_type",
            field=models.CharField(
                choices=[
                    ("SPLIT", "Split"),
                    ("PERSONAL", "Personal"),
                    ("GROUP", "Group"),
                    ("KIDS", "Kids"),
                    ("ONETIME", "One time"),
                ],
                default="ONETIME",
                max_length=63,
            ),
        ),
        migrations.DeleteModel(
            name="SubscriptionType",
        ),
    ]
