from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LogoutView, VdotViewSet, UserDetailView
from .views import LoginView, LogoutView, RefreshTokenView, TokenVerifyView


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'vdots', VdotViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("users/<uid>/", UserDetailView.as_view()),
    # path("logout/", LogoutView.as_view(), name="logout"),

    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("refresh/", RefreshTokenView.as_view(), name="token_refresh"),
]
