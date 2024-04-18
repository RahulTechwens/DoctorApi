from django.db import models
from doctorUser.models import CustomUser
from slotEntry.models import slotEntry

class Slot(models.Model):
    store = models.ForeignKey(slotEntry, on_delete=models.CASCADE, default=None)
    date = models.DateField()
    time = models.TimeField( null=True )
    description = models.TextField( null=True )
    is_complete = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
       return f"Slot {self.id} - {self.date} {self.time} ({'Complete' if self.is_complete else 'Incomplete'})"

class SlotMoney(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField( null=True )
    total_amount = models.TextField( null=True )
    amount = models.TextField( null=True ) 

    def __str__(self):
       return self.id