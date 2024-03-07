from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from .models import (
    Subscription,
    SubscriptionType,
    Visitor,
    TrainingType,
    Trainer,
    Training,
    Signup,
    Discount,
    Schedule,
)
from .serializers import (
    SubscriptionTypeSerializer,
    SubscriptionSerializer,
    SubscriptionListSerializer,
    SubscriptionVisitorSerializer,
    VisitorSerializer,
    TrainingTypeSerializer,
    TrainerSerializer,
    TrainerDetailSerializer,
    TrainerListSerializer,
    TrainingSerializer,
    TrainingDetailSerializer,
    TrainingListSerializer,
    SignupSerializer,
    SignupListSerializer,
    SignupVisitorListSerializer,
    SignupDetailSerializer,
    SignupVisitorSerializer,
    DiscountSerializer,
    ScheduleSerializer
)


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = DiscountSerializer


class SubscriptionTypeViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Subscription.objects.all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(visitor__user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return SubscriptionListSerializer
        if self.request.user.is_staff:
            return SubscriptionSerializer
        return SubscriptionVisitorSerializer

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.is_staff:
            visitor_id = Visitor.objects.get(user_id=request.user.id).id
            serializer.save(visitor_id=visitor_id)
        else:
            serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = (IsAdminUser,)


class TrainingTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainingType.objects.all()
    serializer_class = TrainingTypeSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TrainerListSerializer
        elif self.action == "retrieve":
            return TrainerDetailSerializer
        return TrainerSerializer


class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TrainingListSerializer
        elif self.action == "retrieve":
            return TrainingDetailSerializer
        return TrainingSerializer


class SignupViewSet(viewsets.ModelViewSet):
    queryset = Signup.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Signup.objects.all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(visitor__user=self.request.user)

    def get_serializer_class(self):
        if not self.request.user.is_staff:
            if self.action in ["list", "retrieve"]:
                return SignupVisitorListSerializer
            return SignupVisitorSerializer
        else:
            if self.action == "list":
                return SignupListSerializer
            elif self.action == "retrieve":
                return SignupDetailSerializer
            return SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.is_staff:
            visitor_id = Visitor.objects.get(user_id=request.user.id).id
            serializer.save(visitor_id=visitor_id)
        else:
            serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
