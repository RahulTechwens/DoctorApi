from django.urls import path
from .views import SlotEntryViewSet

urlpatterns = [
  path('slot/entry', SlotEntryViewSet.as_view(), name="slot_entry"),
  path('get/slot/entry',  SlotEntryViewSet.as_view(), name="user_list")
]
