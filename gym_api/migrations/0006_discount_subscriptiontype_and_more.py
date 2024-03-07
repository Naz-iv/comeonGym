# Generated by Django 5.0.3 on 2024-03-06 11:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gym_api", "0005_alter_training_trainer_alter_visitor_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Discount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=63)),
                ("code", models.CharField(max_length=126)),
                ("discount", models.IntegerField(default=0)),
                ("valid_from", models.DateTimeField(blank=True, null=True)),
                ("valid_to", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="SubscriptionType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sub_type", models.CharField(max_length=63)),
                ("number_of_workouts", models.IntegerField()),
                ("price", models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name="subscription",
            name="number_of_workouts",
        ),
        migrations.RemoveField(
            model_name="subscription",
            name="price",
        ),
        migrations.AddField(
            model_name="subscription",
            name="is_activated",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="subscription",
            name="price_with_discount",
            field=models.DecimalField(decimal_places=2, default=280, max_digits=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="visitor",
            name="birthday",
            field=models.DateField(default="2000-01-01"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="visitor",
            name="name",
            field=models.CharField(default="Name", max_length=63),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="visitor",
            name="phone_number",
            field=models.CharField(default="380952563944", max_length=126),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="visitor",
            name="surname",
            field=models.CharField(default="Surname", max_length=63),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="subscription",
            name="activated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="training",
            name="day_of_week",
            field=models.CharField(
                choices=[
                    ("Понеділок", "Понеділок"),
                    ("Вівторок", "Вівторок"),
                    ("Середа", "Середа"),
                    ("Четвер", "Четвер"),
                    ("П'ятниця", "П'ятниця"),
                    ("Субота", "Субота"),
                    ("Неділя", "Неділя"),
                ],
                default="Понеділок",
                max_length=63,
            ),
        ),
        migrations.AlterField(
            model_name="trainingtype",
            name="training_type",
            field=models.CharField(max_length=63),
        ),
        migrations.AlterField(
            model_name="visitor",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="visitor",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="sub_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subscriptions",
                to="gym_api.subscriptiontype",
            ),
        ),
    ]
