from django.urls import path
from .views import SlotBookViewSet, SlotMoneyViewSet

urlpatterns = [
  path('slot/book', SlotBookViewSet.as_view(), name="slot_book"),
  path('slots', SlotBookViewSet.as_view(), name="slot_list"),
  path('add/money', SlotMoneyViewSet.as_view(), name="add_money"),
  path('money', SlotMoneyViewSet.as_view(), name="get_money"),

]
