from django.db import models
from app.accounts.models import User
from django.core.exceptions import ValidationError
import re


EVENT_UNITS_CHOICES = [
    ('800m', '800m'),
    ('1500m', '1500m'),
	('1mile', '1mile'),
    ('3000m', '3000m'),
    ('3000mSC', '3000mSC'),
    ('2mile', '2mile'),
    ('5000m', '5000m'),
    ('10000m', '10000m'),
    ('ハーフマラソン', 'ハーフマラソン'),
    ('フルマラソン', 'フルマラソン'),
]

# タイムフォーマットの正規表現
TIME_FORMATS = [
    r"^\d{1,2}:\d{2}:\d{2}$",  # フルマラソン (例: 2:22:25)
    r"^\d{1,2}'\d{2}\"(?:\d{1,2})?$",  # 1500m (例: 4'12"11)
]


class SpecialtyEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=20, choices=EVENT_UNITS_CHOICES, null=True, blank=True)
    best_time = models.CharField(
        max_length=15,  # マラソン形式（hh:mm:ss）も1500m形式（m'ss"SS）も許容
        null=True,
        blank=True,
        help_text="Format: hh:mm:ss for long distances, m'ss\"SS for middle distances"
    )
    recorded_at = models.DateField(auto_now_add=True)

    """
    class Meta:はモデルのテーブル名を明示的に指定するためのクラス
    デフォルトのテーブル名(specialtyevent)ではなく、specialty_eventに設定する
    """
    class Meta:
        db_table = "specialty_event"
        unique_together = ("user", "event_name")  # ユーザーごとに同じ種目を複数登録不可

    def clean(self):
        """バリデーション: 同じ種目を1ユーザーが複数登録できない & best_time のフォーマットチェック"""
        if self.user and self.pk is None:  # 新規作成時のみチェック
            if SpecialtyEvent.objects.filter(user=self.user, event_name=self.event_name).exists():
                raise ValidationError(f"You can only have one record for {self.event_name}.")

        # best_time のフォーマットチェック
        if self.best_time:
            if not any(re.match(pattern, self.best_time) for pattern in TIME_FORMATS):
                raise ValidationError("Invalid time format. Use hh:mm:ss for long distances or m'ss\"SS for middle distances.")

    def save(self, *args, **kwargs):
        """保存時にバリデーションを適用"""
        self.full_clean()  # すべてのバリデーションを適用
        super().save(*args, **kwargs)
