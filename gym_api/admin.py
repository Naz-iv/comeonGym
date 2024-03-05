from django.contrib import admin
from .models import (
    TrainingType,
    Trainer,
    Subscription,
    Training,
    Visitor,
    Signup,
)

admin.site.register(TrainingType)
admin.site.register(Trainer)
admin.site.register(Subscription)
admin.site.register(Training)
admin.site.register(Visitor)
admin.site.register(Signup)
