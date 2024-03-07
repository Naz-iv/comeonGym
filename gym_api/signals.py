from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


# TODO: Find way to identify correct subscription type for correct training
@receiver(post_save, sender=Signup)
def increment_visit_count(sender, instance, created, **kwargs):
    if created:
        subscription = instance.visitor.subscriptions.filter(is_activated=True).first()
        if subscription:
            subscription.visit_count += 1
            subscription.save()


@receiver(post_delete, sender=Signup)
def decrement_visit_count(sender, instance, **kwargs):
    subscription = instance.visitor.subscriptions.filter(is_activated=True).first()
    if subscription and subscription.visit_count > 0:
        subscription.visit_count -= 1
        subscription.save()
