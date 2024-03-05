from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import (
    Subscription,
    Visitor,
    TrainingType,
    Trainer,
    Training,
    Signup,
)
from .serializers import (
    SubscriptionSerializer,
    VisitorSerializer,
    TrainingTypeSerializer,
    TrainerListSerializer,
    TrainingSerializer,
    SignupSerializer,
)


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer


class TrainingTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainingType.objects.all()
    serializer_class = TrainingTypeSerializer


class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerListSerializer


class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

    @action(detail=True, methods=["get"])
    def signups(self, request, pk=None):
        training = self.get_object()
        signups = training.signups.all()
        serializer = SignupSerializer(signups, many=True)
        return Response(serializer.data)


class SignupViewSet(viewsets.ModelViewSet):
    queryset = Signup.objects.all()
    serializer_class = SignupSerializer
