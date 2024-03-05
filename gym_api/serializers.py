from rest_framework import serializers
from .models import (
    SubscriptionType,
    Subscription,
    Visitor,
    TrainingType,
    Trainer,
    Training,
    Signup,
)


class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = "__all__"


class TrainingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingType
        fields = "__all__"


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = "__all__"

class TrainerDetailSerializer(TrainerSerializer):
    class Meta:
        model = Trainer
        fields = ["id", "name", "surname", "description", "image"]

class TrainerListSerializer(TrainerSerializer):
    training_types = serializers.StringRelatedField(many=True)

    class Meta:
        model = Trainer
        fields = "__all__"


class TrainingSerializer(serializers.ModelSerializer):
    available = serializers.ReadOnlyField()
    trainer = TrainerListSerializer()

    class Meta:
        model = Training
        fields = "__all__"


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signup
        fields = "__all__"
