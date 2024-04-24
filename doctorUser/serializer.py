from rest_framework import serializers
from .models import CustomUser, UserProfile
from slotbook.models import Slot
from slotbook.serializer import SlotSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'address', 'full_name', 'user_id']

class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    slots = SlotSerializer(many=True, read_only=True, source='slot_set')  # Include SlotSerializer for slot details

    class Meta:
        model = CustomUser
        fields = ['id', 'user_name', 'email', 'phone', 'password', 'type', 'create_date', 'profile', 'slots']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = CustomUser.objects.create_user(**validated_data)
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        return user
