from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect

from .models import Order, AvailableDate
from .forms import DateAvailabilityForm

class SetDateAvailability(admin.ModelAdmin):
  list_display = ('id', 'selected_date',)

  class Media:
    css = {
      'all': (
        '/static/css/bootstrap-datepicker3.min.css',
        '/static/css/dataTables.bootstrap4.css',
        '/static/css/responsive.bootstrap4.css',
        '/static/css/admin.css',
      )
    }
    js = ( 
      '/static/js/bootstrap-datepicker.min.js', 
      '/static/js/moment.js',
      '/static/js/moment-timezone-with-data.js',

      '/static/js/dataTables.js',
      '/static/js/dataTables.bootstrap4.js',
      '/static/js/dataTables.responsive.js'
    )

  def has_add_permission(self, request, obj=None):
    return False

  def has_change_permission(self, request, obj=None):
    return False

  def changelist_view(self, request, extra_context=None):
    self.change_list_template = 'admin/change_availability_list.html' 
    if request.method == 'POST':
      selected_dates = [ele for x in request.POST['selectedDates'].split(',') for ele in x.split()]
      for date in selected_dates:
        AvailableDate.objects.create(selected_date=date)
      return HttpResponseRedirect(request.path_info)

    queryset = AvailableDate.objects.all().order_by('selected_date')
    dates_array = [item.selected_date.strftime("%Y-%m-%d") for item in queryset]
    extra_context = extra_context or {}
    extra_context['selected_dates'] = dates_array
    extra_context['dates'] = queryset

    return super().changelist_view(request, extra_context=extra_context)

admin.site.register(AvailableDate, SetDateAvailability)

class ShowBookings(admin.ModelAdmin):
  list_display = ('user_username', 'start_date', 'end_date', 'duration')

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = "Custom Model Name"
    verbose_name_plural = "Custom Model Names"

  def has_add_permission(self, request, obj=None):
    return False

  def has_change_permission(self, request, obj=None):
    return False

  def user_username(self, obj):
    return obj.user.full_name + '(' + obj.user.email + ')'

  user_username.short_description = 'User'

admin.site.register(Order, ShowBookings)
