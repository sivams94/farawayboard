from django import forms
from .models import AvailableDate

class DateAvailabilityForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['selected_date'].initial = self.instance.selected_date

class BookingForm(forms.Form):
  date = forms.DateField()
  start_time = forms.TimeField()
  duration = forms.CharField()

class CouponForm(forms.Form):
  code = forms.CharField(label='Coupon Code')