from rest_framework import serializers
from .models import Slot, SlotMoney, CustomUser
# from doctorUser.serializer import UserProfileSerializer
from doctorUser.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone']

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
    user_info = UserSerializer(source='user', read_only=True)

    class Meta:
        model = SlotMoney
        fields =['id', 'user', 'date', 'time', 'total_amount', 'amount', 'profile', 'user_info']
    