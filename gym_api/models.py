import os
from uuid import uuid4

from django.db import models
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from .choices import DAY_OF_WEEK


def image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(str(instance))}-{uuid4()}{extension}"

    return os.path.join("photos/", filename)


class Visitor(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="visitor",
        null=True,
    )
    name = models.CharField(max_length=63)
    surname = models.CharField(max_length=63)
    birthday = models.DateField()
    phone_number = models.CharField(max_length=126)
    profile_picture = models.ImageField(null=True, blank=True, upload_to=image_file_path)

    def __str__(self):
        return f"{self.name} {self.surname}"


class SubscriptionType(models.Model):
    sub_type = models.CharField(max_length=63)
    number_of_workouts = models.IntegerField()
    price = models.IntegerField()

    class Meta:
        ordering = ["sub_type"]
        unique_together = ["sub_type", "number_of_workouts"]

    def __str__(self):
        return (f"{self.sub_type} | {self.number_of_workouts} "
                f"{'тренування' if self.number_of_workouts < 5 else 'тренувань'}")


class Discount(models.Model):
    name = models.CharField(max_length=63)
    code = models.CharField(max_length=126)
    discount = models.IntegerField(default=0)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} | Знижка: {self.discount}"


class Subscription(models.Model):
    sub_type = models.ForeignKey(SubscriptionType, related_name="subscriptions", on_delete=models.CASCADE)
    brought_at = models.DateTimeField(auto_now_add=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    is_activated = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True)
    visit_count = models.IntegerField(default=0)
    visitor = models.ForeignKey(Visitor, related_name="subscriptions", on_delete=models.CASCADE)
    discount = models.ForeignKey(
        Discount, related_name="subscriptions", on_delete=models.SET_NULL, null=True, blank=True
    )
    price_with_discount = models.DecimalField(decimal_places=2, max_digits=6, default=0)

    def get_price_with_discount(self):
        if self.discount:
            return self.sub_type.price * (1 - (self.discount.discount / 100))
        return self.sub_type.price

    def save(self, *args, **kwargs):
        self.price_with_discount = self.get_price_with_discount()
        super().save(*args, **kwargs)

    @property
    def visits_remaining(self):
        return self.sub_type.number_of_workouts - self.visit_count

    @property
    def expiry_date(self):
        if not self.activated_at:
            return None
        return self.activated_at + relativedelta(months=1)

    def __str__(self):
        return (f"Тип: {self.sub_type} | Залишилось тренувань: {self.visits_remaining} "
                f"| Дійсний до: {self.expiry_date.strftime('%Y-%m-%d %H:%M')}")


class TrainingType(models.Model):
    name = models.CharField(max_length=63)
    duration = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Trainer(models.Model):
    name = models.CharField(max_length=63)
    surname = models.CharField(max_length=63)
    description = models.TextField()
    training_types = models.ManyToManyField(TrainingType, related_name="trainers")
    trainer_photo = models.ImageField(null=True, blank=True, upload_to=image_file_path)

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"

    def __str__(self):
        return self.full_name


class Schedule(models.Model):
    day_of_week = models.CharField(max_length=63, choices=DAY_OF_WEEK, default="Понеділок")
    time = models.TimeField()
    training_type = models.ForeignKey(
        TrainingType, on_delete=models.CASCADE, related_name="schedule"
    )
    trainer = models.ForeignKey(
        Trainer, on_delete=models.SET_NULL, related_name="schedule", null=True
    )
    price = models.IntegerField()
    max_visitors = models.IntegerField(default=10)

    class Meta:
        ordering = ["day_of_week", "time"]
        unique_together = ["day_of_week", "time", "training_type"]

    def __str__(self):
        return (f"{self.day_of_week} | {self.time.strftime('%H:%M')} | {self.training_type.name} "
                f"| {self.trainer.full_name}")


class Training(models.Model):
    date = models.DateField()
    training = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="trainings",
    )

    @property
    def available(self):
        return self.training.max_visitors - self.signups.count()

    class Meta:
        ordering = ["date", "training__time"]
        unique_together = ["date", "training"]

    def __str__(self):
        return f"{self.date} | {self.training} | Вільних місць: {self.available}"


class Signup(models.Model):
    training = models.ForeignKey(
        Training, related_name="signups", on_delete=models.CASCADE
    )
    visitor = models.ForeignKey(
        Visitor, related_name="signups", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ["training", "visitor"]

    def __str__(self):
        return f"{self.training} | {self.visitor}"
    