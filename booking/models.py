from django.db import models
from django.utils.timezone import now
from accounts.models import CustomUser

class Order(models.Model):
  duration = models.CharField(max_length = 200)
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    db_table = 'bookings'
    verbose_name = 'Booking'
    verbose_name_plural = 'Bookings'
    ordering = ['start_date']

class AvailableDate(models.Model):
  selected_date = models.DateField()

  class Meta:
    db_table = 'available_dates'
    app_label = 'booking'

class CancelledDate(models.Model):
  cancelled_date = models.DateField()

  class Meta:
    db_table = 'cancelled_dates'
    app_label = 'booking'
