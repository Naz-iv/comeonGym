from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("subscriptions", views.SubscriptionViewSet)
router.register("visitors", views.VisitorViewSet)
router.register("training-types", views.TrainingTypeViewSet)
router.register("trainers", views.TrainerViewSet)
router.register("schedule", views.TrainingViewSet)
router.register("signups", views.SignupViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # path("schedule/", views.index, name="schedule"),
    # path("trainers/", views.index, name="trainers"),
    # path("trainings/", views.index, name="trainings"),
    # path("prices/", views.index, name="prices"),
]


app_name = "gym"
