import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin
)
from django.contrib.auth.hashers import make_password, check_password


DISTANCE_UNITS_CHOICES = [
    ('km', 'km'),
    ('mile', 'mile'),
    ('m', 'm'),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """通常のユーザーを作成する"""
        if not email:
            raise ValueError('メールアドレスは必須です。')
        if not password:
            raise ValueError('パスワードは必須です。')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 必ずハッシュ化
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル（管理画面は使用しない）"""
    # id（整数）は内部処理用、uuid は外部システムやURL識別用
    uuid = models.UUIDField("UUID", default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField("名前", max_length=30)
    email = models.EmailField("メールアドレス", max_length=255, unique=True)
    password = models.CharField("パスワード", max_length=128)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def set_password(self, raw_password):
        """パスワードをハッシュ化して保存する"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """パスワードが正しいか確認する"""
        return check_password(raw_password, self.password)


class Vdot(models.Model):
    """Vdotの計算に関する情報を格納するモデル"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vdots")
    distance_value = models.FloatField("距離", null=False)
    distance_unit = models.CharField("距離単位", max_length=5, choices=DISTANCE_UNITS_CHOICES, null=False)
    time = models.TimeField("時間", null=False)
    elevation = models.IntegerField("標高", null=True, blank=True)
    temperature = models.IntegerField("気温", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
