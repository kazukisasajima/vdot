from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, VdotViewSet, UserDetailView


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'vdots', VdotViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("users/<uid>/", UserDetailView.as_view()),
]
