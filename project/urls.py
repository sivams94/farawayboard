"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth

# from accounts import views as page_not_found
from accounts import views as accounts_view
from booking import views as booking_view

admin.site.site_header = 'My Admin'
admin.site.site_title = 'My Admin'

urlpatterns = [
  path('admin/', admin.site.urls),

  ##### accounts related path########################## 
  path('', include('accounts.urls')),
  path('login/', accounts_view.Login, name ='login'),
  path('logout/', auth.LogoutView.as_view(template_name ='accounts/login.html'), name = 'logout'),
  path('register/', accounts_view.register, name ='register'),

  ##### accounts related path########################## 
  path('', include('booking.urls')),
  path('booking/', booking_view.index, name ='booking'),
]
