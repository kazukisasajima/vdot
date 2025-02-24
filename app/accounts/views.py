import datetime

from rest_framework.generics import RetrieveAPIView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import User, Vdot
from .serializers import UserSerializer, VdotSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
# from django.contrib.auth import authenticate
# from app.authentication import set_cookie_tokens
from rest_framework.views import APIView
from django.conf import settings
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class LoginView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        # access token set cookie
        access_token = response.data["access"]
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=access_token,
            domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
            path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            expires=datetime.datetime.utcnow() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )

        # refresh token set cookie
        refresh_token = response.data["refresh"]
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
            value=refresh_token,
            domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
            path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            expires=datetime.datetime.utcnow() + settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        return response


class LogoutView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        # アクセストークンのクッキーを削除
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'], domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'], path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'])

        # リフレッシュトークンのクッキーを削除
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'], domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'], path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'])

        return response


class TokenVerifyView(APIView):
    def post(self, request, *args, **kwargs):
        # Authorization ヘッダーからトークンを取得
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])

        if access_token is None:
            return Response({"detail": "Authorization header is missing."}, status=status.HTTP_400_BAD_REQUEST)

        # トークンを検証
        serializer = TokenVerifySerializer(data={"token": access_token})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        # クッキーからリフレッシュトークンを取得
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])

        if refresh_token is None:
            return Response({"detail": "Refresh token is missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # リフレッシュトークンを検証し、新しいアクセストークンとリフレッシュトークンを生成
            refresh = RefreshToken(refresh_token)
            data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }

            # 新しいアクセストークンとリフレッシュトークンをクッキーに設定
            response = Response(data, status=status.HTTP_200_OK)

            # access token set cookie
            access_token = response.data["access"]
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=access_token,
                domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
                expires=datetime.datetime.utcnow() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )

            # refresh token set cookie
            refresh_token = response.data["refresh"]
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
                value=refresh_token,
                domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
                expires=datetime.datetime.utcnow() + settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            return response
        except TokenError as e:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)

# class CustomTokenObtainPairView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = authenticate(username=request.data["email"], password=request.data["password"])
#         if user is None:
#             return Response({"detail": "認証に失敗しました"}, status=status.HTTP_401_UNAUTHORIZED)
        
#         response = Response(serializer.validated_data, status=status.HTTP_200_OK)
#         set_cookie_tokens(response, user)  # Cookie に保存
#         return response


# class LogoutView(APIView):
#     def post(self, request):
#         response = Response({"message": "ログアウトしました"}, status=status.HTTP_200_OK)
#         response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
#         response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
#         return response


class UserViewSet(viewsets.ModelViewSet):
    """ユーザー情報の取得・編集・削除を行うビュー"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # 認証不要で全員アクセス可能（後で変更可能）


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'uuid'


class VdotViewSet(viewsets.ModelViewSet):
    """Vdotのデータを取得・登録・更新・削除するビュー"""
    queryset = Vdot.objects.all()
    serializer_class = VdotSerializer
    permission_classes = [AllowAny]  # 認証不要で全員アクセス可能（後で変更可能）
