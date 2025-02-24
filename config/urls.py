from django.urls import path, include
# from app.accounts.views import CustomTokenObtainPairView 

urlpatterns = [
    # path("api/auth/jwt/create/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    # アカウント
    path("api/auth/", include("app.accounts.urls")), 
    path("api/", include("app.accounts.urls")),
]
