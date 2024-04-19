from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.dateparse import parse_duration
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from datetime import datetime, timedelta, time as dt_time
from .models import Order, AvailableDate, CancelledDate
from .forms import CouponForm
from coupons.models import Coupon
from accounts.models import CustomUser

@login_required(login_url='/login')
def index(request):
  if request.user.is_superuser:
    return redirect('/admin')
  else:
    if request.method == 'POST':
      form_data = {
        'date': request.POST['date'],
        'start_time': request.POST['start_time'],
        'duration': request.POST['duration']
      }
      request.session['booking_form_data'] = form_data
      return redirect('checkout')

    my_bookings = Order.objects.filter(
      end_date__gte=datetime.now(),
      user_id=request.user.id
    )

    for booking in my_bookings:
      if CancelledDate.objects.filter(cancelled_date=booking.start_date.strftime("%Y-%m-%d")).exists():
        booking.status = 'Date cancelled'

    queryset = AvailableDate.objects.filter(selected_date__gte=timezone.localtime().strftime("%Y-%m-%d"))    
    dates_array = [item.selected_date.strftime("%Y-%m-%d") for item in queryset]

    return render(request, 'booking/index.html', {
      'pageTitle': 'Bookings',
      'name': request.user.full_name[0],
      'bookings': my_bookings,
      'selected_dates': dates_array
    })

def checkout(request):
  form_data = request.session.get('booking_form_data')
  coupon_form = CouponForm(request.POST or None)
  valid_coupon_code = request.session.get('coupon_code')
  error_message = None
  success_message = None

  if not form_data:
    return redirect("/booking")

  if request.method == 'POST':
    if coupon_form.is_valid():
      code = coupon_form.cleaned_data['code']
      try:
        if Coupon.objects.filter(code=code, active=1, assign_user_id=request.user.id, is_used_by_booking_id__isnull=True).exists():
          request.session['coupon_code'] = code
          valid_coupon_code = code
          success_message = "Coupon code applied successfully."
        else:
          error_message = "Invalid coupon code."
      except Coupon.DoesNotExist:
        error_message = "Invalid coupon code."
  return render(request, 'booking/checkout.html', {
    'pageTitle': 'Confirm Booking',
    'form_data': form_data,
    'coupon_form': coupon_form,
    'valid_coupon_code': valid_coupon_code,
    'error_message': error_message,
    'success_message': success_message
  })

def booking_confirm(request):
  if request.method == 'POST':
    form_data = request.session.get('booking_form_data')
    split_hours_minutes = form_data.get("duration").split(':')
    valid_coupon_code = request.session.get('coupon_code')

    # Combine date and time into a single datetime object
    combined_startdatetime = datetime.combine(datetime.strptime(form_data.get("date"), '%Y-%m-%d').date(), datetime.strptime(form_data.get("start_time"), "%I:%M %p").time())
    start_datetime = combined_startdatetime
    end_datetime = combined_startdatetime + timedelta(hours=int(split_hours_minutes[0]), minutes=int(split_hours_minutes[1]))

    model_instance = Order(
      start_date=start_datetime,
      end_date=end_datetime,
      duration=form_data.get("duration"),
      user_id=request.user.id
    )
    model_instance.save()

    # Update booking id in coupon
    coupon_instance = Coupon.objects.get(code=valid_coupon_code)
    coupon_instance.is_used_by_booking_id = model_instance.id
    coupon_instance.save()

    del request.session['booking_form_data']
    del request.session['coupon_code']
  return render(request, 'booking/booking_success.html', {
    'pageTitle': 'Booking Success',
  })

def booking_cancel(request):
  if request.method == 'POST':
    del request.session['booking_form_data']
  return redirect("/booking")

def destroy(request, id):  
  booking = Order.objects.get(id=id)  
  booking.delete()  
  return JsonResponse({'deleted':True})

def check_availability(request):
  date = request.POST['date']
  start_time = request.POST['start_time']
  duration = request.POST['duration']

  split_hours_minutes = duration.split(':')

  # Add duration to start_time
  start_time_obj = datetime.strptime(start_time, '%I:%M %p')
  end_time_obj = start_time_obj + timedelta(hours=int(split_hours_minutes[0]), minutes=int(split_hours_minutes[1]))
  end_time_str = datetime.strftime(end_time_obj, '%I:%M %p')

  start_datetime = datetime.strptime(date + ' ' + start_time, '%Y-%m-%d %H:%M %p')
  end_datetime = datetime.strptime(date + ' ' + end_time_str, '%Y-%m-%d %H:%M %p')

  records_within_range = Order.objects.filter(
    start_date__lte=end_datetime,
    end_date__gte=start_datetime
  )

  if records_within_range.exists():
    return JsonResponse({'exists':True})
  else:
    return JsonResponse({'exists':False})

def delete_date(request):
  id = request.POST.get('id')

  booking = AvailableDate.objects.get(id=id)
  filtered_bookings = Order.objects.filter(start_date__date=booking.selected_date)
  user_ids = filtered_bookings.values_list('user_id', flat=True).distinct()
  users = CustomUser.objects.filter(id__in=user_ids).values_list('email', flat=True)

  CancelledDate.objects.create(cancelled_date=booking.selected_date)

  subject = 'Notification for time slot cancellation or non availability due to unforeseen circumstances'
  message = render_to_string('booking/mail/slot_cancellation_notification.html', {})
  recipient_list = list(users)

  send_mail(subject, message, None, recipient_list)

  booking.delete()
  return JsonResponse({'deleted':True})