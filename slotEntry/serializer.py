from rest_framework import serializers
from .models import slotEntry

class SlotEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = slotEntry
        fields = '__all__'
