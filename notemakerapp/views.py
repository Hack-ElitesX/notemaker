from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView

from . import models
import operator
import itertools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User

from .forms import UserForm


def home(request):
    param = {'Name': "TestNotes"}
    return render(request, 'home.html', param)


def login1(request):
    return render(request, 'login1.html')


def conversion(request):
    return render(request, 'conversion.html')


def register1(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # confpassword = request.POST['confPassword']
        # if password == confpassword:
        password = make_password(password)

        a = User(first_name=name, username=username,
                 email=email, password=password)

        a.save()
        messages.success(request, 'Account was created successfully')
        return redirect('login1')

    forms = UserForm()
    context = {
        'forms': forms
    }
    return render(request, 'register1.html', context)
    # return render(request, 'register1.html')
