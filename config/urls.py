from django.urls import path, include

urlpatterns = [
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    # アカウント
    path("api/", include("app.users.urls")),
]
