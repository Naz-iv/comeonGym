from django.db import models
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model

from .choices import (
    SUBSCRIPTION_TYPES_CHOICES,
    NUM_OF_TRAININGS_CHOICES,
    DAY_OF_WEEK,
    TRAINING_TYPE,
)


class Visitor(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="subscriptions",
        null=True,
    )

    def __str__(self):
        return f"{self.user.name} {self.user.surname}"


class Subscription(models.Model):
    sub_type = models.CharField(
        max_length=63, choices=SUBSCRIPTION_TYPES_CHOICES, default="ONETIME"
    )
    number_of_workouts = models.IntegerField(
        choices=NUM_OF_TRAININGS_CHOICES, default=1
    )
    brought_at = models.DateTimeField(auto_now_add=True)
    activated_at = models.DateTimeField(auto_now=True, null=True)
    is_valid = models.BooleanField(default=True)
    visit_count = models.IntegerField(default=0)
    visitor = models.ForeignKey(Visitor, related_name="subscriptions", on_delete=models.CASCADE)
    price = models.IntegerField()

    @property
    def visits_remaining(self):
        return self.number_of_workouts - self.visit_count

    @property
    def expiry_date(self):
        if not self.activated_at:
            return None
        return self.activated_at + relativedelta(months=1)

    def __str__(self):
        return (f"Тип: {self.sub_type} | Залишилось тренувань: {self.visits_remaining} "
                f"| Дійсний до: {self.expiry_date.strftime('%Y-%m-%d %H:%M')}")


class TrainingType(models.Model):
    training_type = models.CharField(max_length=63, choices=TRAINING_TYPE, default="Stretching")
    duration = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.training_type


class Trainer(models.Model):
    name = models.CharField(max_length=63)
    surname = models.CharField(max_length=63)
    description = models.TextField()
    training_types = models.ManyToManyField(TrainingType, related_name="trainers")
    image = models.ImageField()

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"

    def __str__(self):
        return self.full_name


class Training(models.Model):
    day_of_week = models.CharField(max_length=63, choices=DAY_OF_WEEK, default="Monday")
    time = models.TimeField()
    training_type = models.ForeignKey(
        TrainingType, on_delete=models.CASCADE, related_name="schedule"
    )
    trainer = models.ForeignKey(
        Trainer, on_delete=models.SET_NULL, related_name="schedule", null=True
    )
    price = models.IntegerField()
    max_visitors = models.IntegerField(default=10)

    @property
    def available(self):
        return self.max_visitors - self.signups.count()

    class Meta:
        ordering = ["time"]
        unique_together = ["day_of_week", "time", "training_type"]

    def __str__(self):
        return (f"{self.day_of_week} | {self.time.strftime('%H:%M')} | {self.training_type.training_type} "
                f"| {self.trainer.full_name} | Avalable places: {self.available}")


class Signup(models.Model):
    date = models.DateField()
    training = models.ForeignKey(
        Training, related_name="signups", on_delete=models.CASCADE
    )
    visitor = models.ForeignKey(
        Visitor, related_name="signups", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ["date", "training", "visitor"]

    def __str__(self):
        return f"{self.date} | {self.training.training_type} | {self.visitor}"
