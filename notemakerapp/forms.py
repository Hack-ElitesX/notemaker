from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
