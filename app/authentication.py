# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.conf import settings
# from rest_framework.response import Response
# from rest_framework.exceptions import AuthenticationFailed
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class CookieJWTAuthentication(JWTAuthentication):
#     def authenticate(self, request):
#         header = self.get_header(request)
#         if header is None:
#             raw_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])
#             if raw_token is None:
#                 return None

#             try:
#                 validated_token = self.get_validated_token(raw_token)
#                 user = self.get_user(validated_token)
#             except Exception:
#                 raise AuthenticationFailed("Invalid token")

#             # ✅ 修正: `(user, validated_token)` のタプルを返す
#             return (user, validated_token)

#         return super().authenticate(request)

# def set_cookie_tokens(response: Response, user):
#     refresh = RefreshToken.for_user(user)
    
#     # アクセストークンをセット
#     response.set_cookie(
#         key=settings.SIMPLE_JWT["AUTH_COOKIE"],
#         value=str(refresh.access_token),
#         httponly=True,
#         secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
#         samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
#         path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
#     )

#     # リフレッシュトークンをセット
#     response.set_cookie(
#         key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
#         value=str(refresh),
#         httponly=True,
#         secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
#         samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
#         path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
#     )

#     return response
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    """Custom authentication class"""

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
        else:
            access_token = self.get_raw_token(header)
        if access_token is None:
            return None

        validated_token = self.get_validated_token(access_token)
        return self.get_user(validated_token), validated_token