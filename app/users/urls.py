from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, VdotViewSet
from app.users import views 

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'vdots', VdotViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("users/<uid>/", views.UserDetailView.as_view()),
]
