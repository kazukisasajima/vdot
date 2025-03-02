from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Vdot
from .serializers import VdotSerializer
import math
import logging

logger = logging.getLogger(__name__)

class VdotViewSet(ModelViewSet):
    queryset = Vdot.objects.all()
    serializer_class = VdotSerializer
    permission_classes = [IsAuthenticated]


COEFF1 = 0.1894393
COEFF2 = -0.012788
COEFF3 = 0.2989558
COEFF4 = -0.1932605

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_vdot(request, user_id):
    try:
        vdot = Vdot.objects.get(user_id__id=user_id)  # ユーザーIDに基づいてVdotを取得
        distance = distance_unit_conversion(vdot)
        time_in_minutes = time_unit_conversion(vdot)
        velocity = calculate_velocity(distance, time_in_minutes)
        vo2max = calculate_vo2max(time_in_minutes)
        VDOT = calculate_vdot(vo2max, velocity)
        pace_zones = calculate_pace_zones(velocity)
        race_times = predict_race_times(vdot)
        data = VdotSerializer(vdot).data
        data['pace_zones'] = pace_zones
        data['VDOT'] = VDOT
        data['race_times'] = race_times
        return Response(data)
    except Vdot.DoesNotExist:
        return Response({'error': 'Vdot data not found.'}, status=404)


def time_unit_conversion(vdot):
    # 時間を分に変換
    hours, minutes, seconds = vdot.time.hour, vdot.time.minute, vdot.time.second
    time_in_minutes = hours * 60 + minutes + seconds / 60
    return time_in_minutes


def distance_unit_conversion(vdot):
    distance_value =vdot.distance_value
    distance_unit =vdot.distance_unit
    # 距離をメートルに変換
    if distance_unit == 'km':
        distance = distance_value * 1000  # キロメートルをメートルに変換
    elif distance_unit == 'mile':
        distance = distance_value * 1609.34  # マイルをメートルに変換
    else:  # 既にメートル単位である場合
        distance = distance_value
        
    return distance


def calculate_velocity(distance, time_in_minutes):
    velocity = distance / time_in_minutes
    return velocity


def calculate_vo2max(time_in_minutes):
    VO2max_percentage = 0.8 + COEFF1 * math.exp(COEFF2 * time_in_minutes) + COEFF3 * math.exp(COEFF4 * time_in_minutes)
    return VO2max_percentage
        
        
def calculate_vdot(vo2max, velocity):
    VO2 = -4.6 + (0.182258 * velocity) + (0.000104 * velocity**2)
    VDOT = VO2 / vo2max
    return round(VDOT,2)


def calculate_pace_zones(velocity):
    # 各ペースゾーン
    zones = {
        "E": (70, 77),
        "M": (88, None),
        "T": (92.5, None),
        "I": (100.5, None),
        "R": (108.25, None)
    }
    distances = {
        "1mi": 1609.34,
        "1Km": 1000,
        "1200m": 1200,
        "800m": 800,
        "600m": 600,
        "400m": 400,
        "300m": 300,
        "200m": 200,
    }
    pace_zones = {}
    
    for zone, (lower_bound, upper_bound) in zones.items():
        pace_zones[zone] = {}
        for distance, distance_m in distances.items():
            lower_pace = calculate_pace(velocity, lower_bound, distance_m)
            if upper_bound:
                upper_pace = calculate_pace(velocity, upper_bound, distance_m)
            else:
                upper_pace = None
            pace_zones[zone][f'{distance}'] = {"lower_pace": format_pace(lower_pace), "upper_pace": format_pace(upper_pace)}
    return pace_zones


def calculate_pace(velocity, vo2max_percentage, distances):
    # 1kmあたりのペースを計算するロジックを実装する
    # ここでは仮の計算式を用いる
    pace = distances / (velocity * vo2max_percentage / 100)

    return pace


def format_pace(pace):
    if pace:
        # pace（分）をmm:ss形式にフォーマットする
        minutes = int(pace)  # 分
        seconds = int((pace - minutes) * 60)  # 秒
        return f"{minutes:02d}:{seconds:02d}"
    return None


def format_time(time_minutes):
    # タイムを hh:mm:ss 形式にフォーマット
    hours = int(time_minutes // 60)
    minutes = int(time_minutes % 60)
    seconds = int((time_minutes - int(time_minutes)) * 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


def pace_per_km(time_minutes, distance_m):
    # キロメートルあたりのペースを計算
    pace_minutes = time_minutes / (distance_m / 1000)
    pace_seconds = int((pace_minutes - int(pace_minutes)) * 60)
    return f'{int(pace_minutes)}:{pace_seconds:02d} /km'


def predict_race_times(vdot):
    # 異なる距離に対する予想タイムを計算
    target_time = time_unit_conversion(vdot)
    target_distance = distance_unit_conversion(vdot)
    distances_m = {
        'マラソン': 42195,
        'ハーフマラソン': 21097.5,
        '30Km': 30000,
        '10Mile': 16093.4,
        '15Km': 15000,
        '10Km': 10000,
        '8Km': 8000,
        '6Km': 6000,
        '5Km': 5000,
        '2Mile': 3218.69,
        '3200m': 3200,
        '3Km': 3000,
        '1Mile': 1609.34,
        '1600m': 1600,
        '1500m': 1500,
    }
    race_times = {}
    for race, distance in distances_m.items():
        # 予想タイムの計算
        if distance == target_distance:
            predicted_time_minutes = target_time
        else:
            predicted_time_minutes = target_time * (distance / target_distance)**1.06

        # タイムを hh:mm:ss 形式にフォーマット（四捨五入を含む）
        hours, remainder = divmod(predicted_time_minutes, 60)
        minutes, seconds = divmod(remainder * 60, 60)  # 分の小数部を秒に変換
        seconds = round(seconds)  # 秒を四捨五入

        # 秒が60になった場合の処理
        if seconds >= 60:
            seconds -= 60
            minutes += 1
        # 分が60になった場合の処理
        if minutes >= 60:
            minutes -= 60
            hours += 1

        formatted_time = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        
        # ペースの計算
        pace_per_km = (predicted_time_minutes / (distance / 1000))
        formatted_pace_per_km = f"{int(pace_per_km)}:{int((pace_per_km - int(pace_per_km)) * 60):02d} /km"
        
        race_times[race] = {
            'predictTime': formatted_time,
            'pacePerKm': formatted_pace_per_km,
        }
    
    return race_times
