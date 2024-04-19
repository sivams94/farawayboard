from django.db import models
from accounts.models import CustomUser
from booking.models import Order

class Coupon(models.Model):
  coupon_name = models.CharField(max_length = 200)
  code = models.CharField(max_length=50, unique=True)
  assign_user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='coupons', null=True, blank=True)
  active = models.BooleanField(default=True)
  is_used_by_booking = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name='coupons', null=True, blank=True)

  class Meta:
    db_table = 'coupons'
    app_label = 'coupons'

  def __str__(self):
    return self.code
