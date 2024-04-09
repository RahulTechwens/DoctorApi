from django.urls import path
from .views import SlotBookViewSet

urlpatterns = [
  path('slot/book', SlotBookViewSet.as_view(), name="slot_book"),
  path('slots', SlotBookViewSet.as_view(), name=("slot_list"))
]
