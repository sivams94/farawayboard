from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
 
urlpatterns = [
  path('', views.index, name ='index'),
  path('accounts/login/', views.index, name='login'),
  path('captcha/', include('captcha.urls')),
  path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
  path('logout/', views.logout, name ='logout'),

  path('accounts/', include('django.contrib.auth.urls')),
]