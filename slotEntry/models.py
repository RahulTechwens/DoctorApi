from django.db import models

class slotEntry(models.Model):
    name = models.CharField(max_length=100, null=True)
    date = models.DateTimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    limit = models.IntegerField(default=6)
    seat_available = models.IntegerField(default=0)


    def __str__(self):
        return f"Slot Entry - Date: {self.date}, Start Time: {self.start_time}, End Time: {self.end_time}"