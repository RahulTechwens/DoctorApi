from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import SlotEntrySerializer
from .models import slotEntry

class SlotEntryViewSet(APIView):
    def post(self, request):
        try:
            data = request.data
            slot_entry_serializer = SlotEntrySerializer(data=data)
            if slot_entry_serializer.is_valid():
                slot_entry_serializer.save()
                return Response({'status': 200, 'success': True, 'message': "Slot Entry Successful"})
            else:
                return Response(slot_entry_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            error_response = {'message': 'An error occurred while entry of Slot', 'error': str(e)}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            slot_entries = slotEntry.objects.filter()
            slot_entry_serializer = SlotEntrySerializer(slot_entries, many=True)
            return Response({'status': 200, 'success': True, 'data': slot_entry_serializer.data})
        except Exception as e:
            error_response = {'message': 'Something went wrong', 'error': str(e)}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)