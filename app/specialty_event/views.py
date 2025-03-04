from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import SpecialtyEvent
from .serializers import SpecialtyEventSerializer
import logging

logger = logging.getLogger(__name__)


class SpecialtyEventViewSet(ModelViewSet):
    queryset = SpecialtyEvent.objects.all()
    serializer_class = SpecialtyEventSerializer
    permission_classes = [IsAuthenticated]
