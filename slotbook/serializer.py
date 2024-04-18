from rest_framework import serializers
from .models import Slot, SlotMoney

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'

class SlotMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotMoney
        fields = '__all__'