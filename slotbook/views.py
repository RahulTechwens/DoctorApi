from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import SlotSerializer
from .models import Slot
from slotEntry.models import slotEntry
from slotEntry.serializer import SlotEntrySerializer

class SlotBookViewSet(APIView):
    def get(self, request):
        try:
            date_string = request.query_params.get('date')
            user_id = request.query_params.get('user_id')  # Corrected typo here
            if date_string:
                search_date = datetime.strptime(date_string, '%Y-%m-%d').date()
                slots = Slot.objects.filter(date=search_date, user_id=user_id)
            else:
                slots = Slot.objects.filter(user=user_id)  # Corrected typo here
            slot_serializer = SlotSerializer(slots, many=True)
            return Response({'status': 200, 'success': True, 'data': slot_serializer.data})
        except Exception as e:
            error_response = {'status': 400, 'success': False, 'message': 'An error occurred while fetching slots'}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        try:
            data = request.data
            # data['description'] = ""
            data['is_complete'] = False
            slot_book_serialize = SlotSerializer(data=data)
            slot_book_serialize.is_valid(raise_exception=True)
            slot_book_serialize.save()

            slot_seat_available = slotEntry.objects.filter(id=data.get('store')).first()
            serialized_data = SlotEntrySerializer(slot_seat_available).data
            seat_available_value = serialized_data.get('seat_available')

            if seat_available_value != 0:
                slotEntry.objects.filter(id=data.get('store')).update(seat_available=max(seat_available_value - 1, 0))

                return Response({'status': 200, 'success': True, 'message': 'Slot Booked Successful', 'data': max(seat_available_value - 1, 0)})
            else:
                return Response({'status': 404, 'success': False, 'message': 'Slot are not available'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            error_response = {'message': 'An error occurred while creating the user', 'e': str(e)}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        