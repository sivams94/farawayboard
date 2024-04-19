from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from . import views
from django.conf.urls.static import static
 
urlpatterns = [
  path('', views.index, name ='index'),

  path('checkout/', views.checkout, name='checkout'),
  path('booking_confirm/', views.booking_confirm, name='booking_confirm'),
  path('booking_cancel/', views.booking_cancel, name='booking_cancel'),
  path('bookings/delete/<int:id>', views.destroy),
  path('check_availability', views.check_availability),
  path('delete_date/', views.delete_date, name='delete_date'),
]