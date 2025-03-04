from django.test import TestCase
from django.core.exceptions import ValidationError
from app.accounts.models import User  # カスタムユーザー
from app.specialty_event.models import SpecialtyEvent  # モデルのインポート

class SpecialtyEventModelTest(TestCase):

    def setUp(self):
        """ テスト用のユーザーを作成 """
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            name="Test User"
        )

    def test_create_valid_specialty_event(self):
        """ 正しいデータで SpecialityEvent を作成できるか """
        event = SpecialtyEvent.objects.create(user=self.user, event_name="1500m", best_time="4'12\"11")
        self.assertEqual(SpecialtyEvent.objects.count(), 1)  # レコードが1つ作成されているか
        self.assertEqual(event.best_time, "4'12\"11")  # best_time が正しく保存されているか

    def test_duplicate_event_name_for_same_user(self):
        """ 同じユーザーが同じ種目を2回登録しようとすると `ValidationError` になるか """
        SpecialtyEvent.objects.create(user=self.user, event_name="1500m", best_time="4'12\"11")
        duplicate_event = SpecialtyEvent(user=self.user, event_name="1500m", best_time="4'10\"00")

        with self.assertRaises(ValidationError) as context:
            duplicate_event.full_clean()  # `clean()` のバリデーションを適用
        self.assertIn("You can only have one record for 1500m.", str(context.exception))

    def test_different_user_can_have_same_event(self):
        """ 別のユーザーなら同じ種目を登録できるか """
        other_user = User.objects.create_user(email="other@example.com", password="password", name="Other User")

        SpecialtyEvent.objects.create(user=self.user, event_name="1500m", best_time="4'12\"11")
        SpecialtyEvent.objects.create(user=other_user, event_name="1500m", best_time="4'20\"00")  # 別のユーザー

        self.assertEqual(SpecialtyEvent.objects.count(), 2)

    def test_invalid_best_time_format(self):
        """ 不正な `best_time` フォーマットが `ValidationError` を引き起こすか """
        event = SpecialtyEvent(user=self.user, event_name="1500m", best_time="4:12.11")  # フォーマットが間違っている
        with self.assertRaises(ValidationError) as context:
            event.full_clean()  # `full_clean()` を呼び出すと `clean()` も実行される
        self.assertIn("Invalid time format", str(context.exception))

    def test_create_specialty_event_without_best_time(self):
        """ `best_time` を空で作成できるか確認 """
        event = SpecialtyEvent.objects.create(user=self.user, event_name="1500m", best_time=None)
        self.assertEqual(SpecialtyEvent.objects.count(), 1)
        self.assertIsNone(event.best_time)  # None のまま保存されているか

    def test_delete_specialty_event(self):
        """ `SpecialtyEvent` を削除できるか """
        event = SpecialtyEvent.objects.create(user=self.user, event_name="1500m", best_time="4'12\"11")
        event.delete()
        self.assertEqual(SpecialtyEvent.objects.count(), 0)  # 削除されているか
