from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("subscriptions", views.SubscriptionViewSet)
router.register("visitors", views.VisitorViewSet)
router.register("training-types", views.TrainingTypeViewSet)
router.register("trainers", views.TrainerViewSet)
router.register("trainings", views.TrainingViewSet)
router.register("signups", views.SignupViewSet)
router.register("prices", views.SubscriptionTypeViewSet)
router.register("discounts", views.DiscountViewSet)
router.register("schedule", views.ScheduleViewSet)


urlpatterns = [
    path("", include(router.urls)),
]


app_name = "gym"
