from rest_framework import serializers
from django.contrib.auth import get_user_model


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("email", "password")

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
