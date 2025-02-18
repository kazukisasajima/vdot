from rest_framework.generics import RetrieveAPIView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import User, Vdot
from .serializers import UserSerializer, VdotSerializer


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
