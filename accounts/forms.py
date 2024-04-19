from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
 
class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()
  captcha = CaptchaField()
  
  class Meta:
    model = get_user_model()
    fields = ['full_name', 'email']

  def __init__(self, *args, **kwargs):
    super(UserRegisterForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.layout = Layout(
      Field('full_name', autofocus=True)
    )

class LoginForm(forms.Form):
  username = forms.EmailField(label='Email', required=True)
  password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)

  def __init__(self, *args, **kwargs):
    super(LoginForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.layout = Layout(
      Field('username', autofocus=True)
    )