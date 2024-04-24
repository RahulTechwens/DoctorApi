from django.urls import path
from .views import TransactionViewSet, PatientViewSet

urlpatterns = [ 
    path('transaction/report', TransactionViewSet.as_view(), name="transaction"),
    path('patient/report',PatientViewSet.as_view(), name="patient" )
]