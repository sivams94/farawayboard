from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
  # change_list_template = 'admin/change_user_list.html'

  model = CustomUser
  list_display = ('full_name', 'email', 'is_active', 'is_superuser', 'date_joined', 'last_login')
  # list_filter = ()
  add_fieldsets = (
    (
      None,
      {
        'classes': ('wide',),
        'fields': ('full_name', 'email', 'password1', 'password2'),
      },
    ),
  )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
