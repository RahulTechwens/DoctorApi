from rest_framework import serializers
from .models import Slot, SlotMoney
# from doctorUser.serializer import UserProfileSerializer
from doctorUser.models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'address', 'full_name', 'user_id']


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'

class SlotMoneySerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(source='user.profile', read_only=True)
    class Meta:
        model = SlotMoney
        fields =['id', 'user', 'date', 'time', 'total_amount', 'amount', 'profile']
    