from rest_framework import serializers
from .models import User, Vdot


class UserSerializer(serializers.ModelSerializer):
    """ユーザー情報のシリアライザー"""
    
    class Meta:
        model = User
        fields = ("id","uuid", "name", "email", "created_at", "updated_at")


class VdotSerializer(serializers.ModelSerializer):
    """Vdotのデータを扱うシリアライザー"""

    class Meta:
        model = Vdot
        fields = fields = ('id', 'user_id', 'distance_value', 'distance_unit', 'time', 'elevation', 'temperature')

    def validate_distance_value(self, value):
        """距離が0以上であることをバリデーション"""
        if value <= 0:
            raise serializers.ValidationError("距離は0より大きい値を指定してください。")
        return value

# class VdotSerializer(serializers.ModelSerializer):
#     # uuidフィールドは読み取り専用
#     uuid = serializers.CharField(read_only=True)
#     # Userモデルのシリアライザーを組み込み(読み取り専用)
#     user = UserSerializer(read_only=True)

#     class Meta:
#         model = Vdot
#         fields = "__all__"