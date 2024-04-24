from django.urls import path
from .views import TransactionViewSet

urlpatterns = [ 
    path('transaction/report', TransactionViewSet.as_view(), name="transaction")
]