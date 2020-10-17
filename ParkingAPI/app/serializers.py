from app.models import Parking
from rest_framework import serializers

class ParkingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Parking
        fields = ('address', 'is_free') #сюда в случае необходимости можно дописать поле с координатами

