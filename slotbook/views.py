from django.shortcuts import render
from rest_framework.views import APIView
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from .serializer import SlotSerializer, SlotMoneySerializer
from .models import Slot, SlotMoney
from slotEntry.models import slotEntry
from slotEntry.serializer import SlotEntrySerializer
from django.db.models import Count
from django.db.models import Q
from django.db.models import Sum

class SlotBookViewSet(APIView):
    def get(self, request):
        try:
            slots = None
            
            date_string = request.query_params.get('date')
            user_id = request.query_params.get('user_id')
            mode = request.query_params.get('mode')
            slot_entries = slotEntry.objects.all()
            slot_entry_serializer = SlotEntrySerializer(slot_entries, many=True).data
            
            if date_string and user_id:

                if mode == 'entry':
                    slot_serializer = [] 
                    search_date = datetime.strptime(date_string, '%Y-%m-%d').date()
                    slot_entries_filter = slotEntry.objects.all()
                    slot_entry_serializer = SlotEntrySerializer(slot_entries_filter, many=True).data
                    for slot_entry_key in slot_entry_serializer:
                        count_book = Slot.objects.filter(store=slot_entry_key["id"], date=search_date)
                        kk = Slot.objects.filter(user=user_id, date=search_date, store=slot_entry_key["id"])
                        slot_serializer_count = SlotSerializer(count_book, many=True).data
                        slot_serializer_data = SlotSerializer(kk, many=True).data

                        if len(slot_serializer_data) > 0:
                            slot_entry_key['is_user_booking'] = 1 
                        else: 
                            slot_entry_key['is_user_booking'] = 0
                            
                        slot_entry_key['seat_available'] = slot_entry_serializer[0]['limit'] - len(slot_serializer_count)
                    return Response({
                        'status': 200,
                        'success': True,
                        'user_wise_slot_register': slot_entry_serializer
                    })


                if mode == 'edit':
                    print("edit")
                    search_date = datetime.strptime(date_string, '%Y-%m-%d').date()
                    slot_entries_filter = slotEntry.objects.all()
                    slot_entry_serializer = SlotEntrySerializer(slot_entries_filter, many=True).data
                    slots = []

                    date_with_data = Slot.objects.filter(user=user_id, date=search_date)
                    slot_serializer_data_date = SlotSerializer(date_with_data, many=True).data
                    print(len(slot_serializer_data_date))
                    if len(slot_serializer_data_date) > 0:


                        for slot_entry_key in slot_entry_serializer:
                            count_book = Slot.objects.filter(store=slot_entry_key["id"], date=search_date)
                            kk = Slot.objects.filter(user=user_id, date=search_date, store=slot_entry_key["id"])
                            slot_serializer_count = SlotSerializer(count_book, many=True).data
                            slot_serializer_data = SlotSerializer(kk, many=True).data

                        
                            slot_data = {
                                'id': slot_entry_key["id"],
                                'name': slot_entry_key["name"],
                                'date': slot_entry_key["date"],
                                'start_time': slot_entry_key["start_time"],
                                'end_time': slot_entry_key["end_time"],
                                'limit': slot_entry_key["limit"],
                                'seat_available': slot_entry_key["limit"] - len(slot_serializer_count),
                                'is_user_booking': 1 if len(slot_serializer_data) > 0 else 0
                            }

                            # if len(slot_serializer_data) > 0:
                            slots.append(slot_data)
                    return Response({
                        'status': 200,
                        'success': True,
                        'user_wise_slot_booked': slots
                    })
        
            else:
                return Response({
                    'status': 200,
                    'success': True,
                    'user_wise_slot_booked': "Wrong Params"
                })

            # for slot_data in slot_entry_serializer:
            #     slot_data["is_user_booking"] = 0
            #     for slot_entry in slots:
            #         found_match = 0
            #         for slot in slot_entry["slots"]:
            #             if slot_data["id"] == slot["slot"]:
            #                 slot_data["is_user_booking"] = 1
            #                 found_match = 1
            #                 break
            #         if not found_match:
            #             slot_data["is_user_booking"] = 0


            # return Response({
            #     'status': 200, 
            #     'success': True, 
            #     'user_wise_slot_booked':slot_entry_serializer, 
            #     # 'slots':slot_serializer.data
            # })
        except Exception as e:
            error_response = {
                'status': 400, 
                'success': False, 
                'message': 'An error occurred while fetching slots',
                'error' : str(e)
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        try:

            # fecthing requested Data
            data = request.data
            data['is_complete'] = False

            # extracting data
            date = data.get('date')
            store = data.get('store')
            user = data.get('user')
            typeof = data.get('typeof')


            # Fetching data acc to slot id
            slot_entries = slotEntry.objects.get(id=store)
            slot_entry_serializer_limit = SlotEntrySerializer(slot_entries, many=False).data['limit']

            # Fetching slot booked acc to date and slot 
            slot_booked = Slot.objects.filter(date=date, store=store)
            slot_book_serializer = SlotSerializer(slot_booked, many=True)

            # Fetching slot booked acc to user and date
            slot_booked_user = Slot.objects.filter(user=user, date=date)
            slot_booked_user_serializer = SlotSerializer(slot_booked_user, many=True).data
            print(slot_booked_user_serializer)
            
            if typeof == 'reschedule':
                if len(slot_book_serializer.data) < slot_entry_serializer_limit:
                    # slots = Slot.objects.filter(date_field=date, user=user)
                    if 'typeof' in data:
                        del data['typeof']
                    slot_booked_user.update(**data)
                    # slot_book_serialize.is_valid(raise_exception=True)
                    # slot_book_serialize.save()

                    return Response({
                        'status': 200, 
                        'success': True, 
                        'message': 'Slot rescheduled Successful',
                    })
                else:

                    return Response({
                        'status': 404, 
                        'success': False, 
                        'message': 'Slots are full.',
                    })
            else:

                # check wheather the user is having any booking for the particular date
                if len(slot_booked_user_serializer) == 0:
                    # checking the slot are full not
                    if len(slot_book_serializer.data) < slot_entry_serializer_limit:
                        slot_book_serialize = SlotSerializer(data=data)
                        slot_book_serialize.is_valid(raise_exception=True)
                        slot_book_serialize.save()
                    else:

                        return Response({
                            'status': 404, 
                            'success': False, 
                            'message': 'Slots are full.',
                        })
                else:
                    return Response({
                        'status': 404, 
                        'success': False, 
                        'message': 'Slot is already booked for the User.',
                    })

            
            
            return Response({
                'status': 200, 
                'success': True, 
                'message': 'Slot Booked Successful',
            })
          
        except Exception as e:
            error_response = {'message': 'An error occurred while creating the user', 'e': str(e)}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        

class SlotMoneyViewSet(APIView):
    def post(self, request):
        try:
            data = request.data
            data['total_amount'] = "5000"

            user = data.get('user')
            paid_amount = float(data.get('amount'))
            total_paid_amount = SlotMoney.objects.filter(user=user).aggregate(total_amount=Sum('amount'))['total_amount']
            summation = paid_amount + total_paid_amount

            total_amount_float = float(data['total_amount'])

            if total_amount_float < summation:
                return Response({
                    'status': 200, 
                    'success': True, 
                    'message': 'Paid amount cannot be greater than Total amount'
                })

            slot_money_serialize = SlotMoneySerializer(data=data)
            slot_money_serialize.is_valid(raise_exception=True)
            slot_money_serialize.save()

            return Response({
                'status': 200, 
                'success': True, 
                'message': 'Money Added Successful',
                'data':summation
            })
        except Exception as e:
            error_response = {'message': 'An error occurred while addmin money', 'e': str(e)}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        try:
            user_id = request.query_params.get('user_id')
            user_money_filter = SlotMoney.objects.filter(user=user_id)
            user_money_serializer = SlotMoneySerializer(user_money_filter, many=True).data
            return Response({
                'status': 200, 
                'success': True, 
                'message': 'Money Added Successful',
                'data':user_money_serializer
            })
        except Exception as e:
            error_response = {'message': 'An error occurred while fetching money', 'e': str(e)}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
