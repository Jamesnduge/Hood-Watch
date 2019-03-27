from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from pyuploadcare.dj.forms import FileWidget
from pyuploadcare.dj.models import ImageField

User = get_user_model()
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        