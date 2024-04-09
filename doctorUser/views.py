from django.db import transaction
from django.utils.text import slugify
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .serializer import *
from .models import *



class UserViewSet(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            data['password'] = '1234'
            data['user_name'] = slugify(data['full_name'])
            
            user_serializer = CustomUserSerializer(data=data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            
            profile_data = {
                'address': data.get('address', ''),
                'full_name': data.get('full_name', '')
            }
            profile_serializer = UserProfileSerializer(data=profile_data)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save(user=user)

            return Response({'status': 200, 'success':True, 'message': 'User created successfully'})
        
        except Exception as e:
            error_response = {
                'success': False
            }
            if 'email' in user_serializer.errors:
                error_response['message'] = 'Email already exists'
            elif 'phone' in user_serializer.errors:
                error_response['message'] = 'Phone number already exists'
            else:
                error_response['message'] = 'An error occurred while creating the user'
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request):
        search_query = request.query_params.get('search', None)
        if search_query:
            users = CustomUser.objects.filter(
                Q(phone__icontains=search_query) | Q(profile__full_name__icontains=search_query)
            )
        else:
            users = CustomUser.objects.all()

        user_serializer = CustomUserSerializer(users, many=True)

        return Response({"data": user_serializer.data}, status=status.HTTP_200_OK)