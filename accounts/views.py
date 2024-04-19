from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from .forms import LoginForm, UserRegisterForm
from .token import account_activation_token

def index(request):
  if request.user.is_authenticated:
    return redirect('booking')
  else:
    return redirect('login')

def Login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    form = LoginForm(request.POST)
    if form.is_valid():
      user = authenticate(request, username = username, password = password)
      print('user---', user)
      if user is not None:
        if user.is_active:
          form = login(request, user)
          return redirect('index')
        else:
          messages.error(request, f'Your account is disabled.')
      else:
        messages.error(request, f'Invalid email or password.')
    else:
      return render(request, "accounts/login.html", {'form': form, 'pageTitle': 'Login'})
  form = LoginForm()
  return render(request, 'accounts/login.html', {'form': form, 'pageTitle': 'Login'})

def register(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.is_active = False
      user.save()

      # send email verification
      current_site = get_current_site(request)
      to_email = form.cleaned_data.get('email')
      subject = "Verify Email"
      message = render_to_string('accounts/email_confirmation.html', {
        'request': request,
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
      })
      email = EmailMessage(
        subject, message, to=[to_email]
      )
      email.content_subtype = 'html'
      email.send()

      messages.success(request, f'Please confirm your email address to complete the registration')
      return redirect('register')
    else:
      return render(request, "accounts/register.html", {'form': form})  
  else:
    form = UserRegisterForm()
  return render(request, 'accounts/register.html', {'form': form, 'pageTitle': 'Register'})

def activate(request, uidb64, token):
  User = get_user_model()
  try:  
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
    user = None
  if user is not None and account_activation_token.check_token(user, token):
    user.is_active = True
    user.save()
    return HttpResponse('Thank you for validating your email address, your registration with farawayboard.com is complete now.') 
  else:
    return HttpResponse('The link is invalid.')

def logout(request):
  return render(request, 'accounts/logout.html')