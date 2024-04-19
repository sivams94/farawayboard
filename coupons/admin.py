import string
import random
from django.contrib import admin
from .models import Coupon
from accounts.models import CustomUser
from django_select2.forms import Select2Widget

class CouponAdmin(admin.ModelAdmin):
  list_display = ['coupon_name', 'code', 'assign_user', 'active']
  list_filter = ['active']
  search_fields = ['code']
  exclude = ('code', 'is_used_by_booking',)

  def get_queryset(self, request):
    qs = super().get_queryset(request)
    if request.user.is_superuser:
      return qs
    else:
      return qs.filter(assign_user=request.user)

  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == "assign_user":
      kwargs["queryset"] = CustomUser.objects.filter(is_superuser=False)
      kwargs["widget"] = Select2Widget
    return super().formfield_for_foreignkey(db_field, request, **kwargs)

  def save_model(self, request, obj, form, change):
    length = 10
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    while Coupon.objects.filter(code=code).exists():
      code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    obj.code = code
    super().save_model(request, obj, form, change)

admin.site.register(Coupon, CouponAdmin)