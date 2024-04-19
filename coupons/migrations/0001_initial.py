# Generated by Django 5.0.3 on 2024-04-18 18:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('booking', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('assign_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='coupons', to=settings.AUTH_USER_MODEL)),
                ('is_used_by_booking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='coupons', to='booking.order')),
            ],
            options={
                'db_table': 'coupons',
            },
        ),
    ]
