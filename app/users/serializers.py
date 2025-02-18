from rest_framework import serializers
from .models import User, Vdot


class UserSerializer(serializers.ModelSerializer):
    """ユーザー情報のシリアライザー"""
    
    class Meta:
        model = User
        fields = ("uuid", "name", "email", "created_at", "updated_at")


class VdotSerializer(serializers.ModelSerializer):
    """Vdotのデータを扱うシリアライザー"""

    class Meta:
        model = Vdot
        fields = "__all__"

    def validate_distance_value(self, value):
        """距離が0以上であることをバリデーション"""
        if value <= 0:
            raise serializers.ValidationError("距離は0より大きい値を指定してください。")
        return value
