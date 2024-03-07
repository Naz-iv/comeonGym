from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import (
    Subscription,
    SubscriptionType,
    Visitor,
    TrainingType,
    Trainer,
    Training,
    Signup,
    Discount,
    Schedule
)


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"


class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class SubscriptionListSerializer(SubscriptionSerializer):
    sub_type = serializers.StringRelatedField()
    class Meta:
        model = Subscription
        fields = [
            "id",
            "brought_at",
            "is_activated",
            "activated_at",
            "is_valid",
            "visit_count",
            "price_with_discount",
            "sub_type"
        ]


class SubscriptionVisitorSerializer(SubscriptionSerializer):
    discount = serializers.CharField(source="discount.code", allow_null=True)

    class Meta:
        model = Subscription
        fields = ["sub_type", "discount"]

    def validate(self, attrs):
        discount_code = attrs.get("discount").get("code")

        if discount_code:
            try:
                discount = Discount.objects.get(code=discount_code)
                attrs["discount"] = discount
            except Discount.DoesNotExist:
                raise serializers.ValidationError(f"Discount code {discount_code} is not valid!")

        return super().validate(attrs)


class VisitorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Visitor
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"


class ScheduleListSerializer(serializers.ModelSerializer):
    trainer = serializers.StringRelatedField()
    training_type = serializers.StringRelatedField()

    class Meta:
        model = Schedule
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
    training_types = serializers.StringRelatedField(many=True)

    class Meta:
        model = Trainer
        fields = ["id", "name", "surname", "description", "trainer_photo", "training_types"]


class TrainerListSerializer(TrainerSerializer):
    class Meta:
        model = Trainer
        fields = ["id", "name", "surname", "description", "trainer_photo"]


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = "__all__"

    def validate(self, attrs):
        days_mapping = {
            "Monday": "Понеділок",
            "Tuesday": "Вівторок",
            "Wednesday": "Середа",
            "Thursday": "Четвер",
            "Friday": "П'ятниця",
            "Saturday": "Субота",
            "Sunday": "Неділя",
        }

        date = attrs.get("date")

        training = attrs.get("training")
        if date and training:
            provided_day = days_mapping.get(date.strftime('%A'))
            if training.day_of_week != provided_day:
                raise serializers.ValidationError(
                    f"Обрана дата ({date}|{provided_day}) не відповідає "
                    f"дню тренування ({training.day_of_week})."
                )
        return super().validate(attrs)


class TrainingDetailSerializer(TrainingSerializer):
    training = ScheduleSerializer()
    visitors = serializers.SerializerMethodField()
    available = serializers.IntegerField()

    class Meta:
        model = Training
        fields = "__all__"

    def get_visitors(self, obj):
        signups = Signup.objects.filter(training=obj)
        visitor_names = [str(signup.visitor) for signup in signups]
        return visitor_names


class TrainingListSerializer(TrainingSerializer):
    training = serializers.StringRelatedField()
    max_visitors = serializers.CharField(source="training.max_visitors")

    class Meta:
        model = Training
        fields = [
            "id",
            "date",
            "training",
            "max_visitors",
            "available"
        ]


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signup
        fields = "__all__"


class SignupListSerializer(SignupSerializer):
    training = serializers.StringRelatedField()
    visitor = serializers.StringRelatedField()

    class Meta:
        model = Signup
        fields = "__all__"


class SignupVisitorListSerializer(SignupSerializer):
    training = TrainingListSerializer()

    class Meta:
        model = Signup
        fields = ["id", "training"]


class SignupDetailSerializer(SignupSerializer):
    training = TrainingListSerializer()
    visitor = VisitorSerializer()

    class Meta:
        model = Signup
        fields = "__all__"


class SignupVisitorSerializer(SignupSerializer):
    class Meta:
        model = Signup
        fields = ["training"]
