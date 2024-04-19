from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Coupon

@receiver(post_save, sender=Coupon)
def send_coupon_email(sender, instance, created, **kwargs):
  if created:
    subject = 'Coupon Created for You!'
    message = render_to_string('coupons/mail/new_coupon.html', {
      'user_name': instance.assign_user.full_name,
      'code': instance.code,
    })
    recipient = instance.assign_user.email
    send_mail(subject, message, None, [recipient])