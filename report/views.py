from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date  

from slotbook.models import SlotMoney
from slotbook.serializer import SlotMoneySerializer
from doctorUser.models import CustomUser
from doctorUser.serializer import CustomUserSerializer

class TransactionViewSet(APIView):
    def get(self, request):
        try:
            from_date_str = request.query_params.get('from_date')
            to_date_str = request.query_params.get('to_date')
            filter = request.query_params.get('filter')

            if filter == 'custom':
                from_date = date.fromisoformat(from_date_str) if from_date_str else None
                to_date = date.fromisoformat(to_date_str) if to_date_str else None
                if from_date and to_date:
                    transaction_report_model = SlotMoney.objects.filter(date__range=[from_date, to_date])
            if filter == 'today':
                today = date.today()
                transaction_report_model = SlotMoney.objects.filter(date=today)
            if filter == 'all':
                transaction_report_model = SlotMoney.objects.all()

            transction_report_serializer = SlotMoneySerializer(transaction_report_model, many=True).data
            return Response({
                'status': 200,
                'success': True,
                'data': transction_report_serializer
            })

        
        except Exception as e:

            error_response = {
                'status': 400, 
                'success': False, 
                'message': 'An error occurred while fetching report',
                'error' : str(e)
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

class PatientViewSet(APIView):
    def get(self, request):
        try:
            users = CustomUser.objects.all()
            user_serializer = CustomUserSerializer(users, many=True).data
            
            return Response({
                'status': 200,
                'success': True,
                'data': user_serializer
            })

        except Exception as e:

            error_response = {
                'status': 400, 
                'success': False, 
                'message': 'An error occurred while fetching report',
                'error' : str(e)
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

