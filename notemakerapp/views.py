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
from .models import NewUser


def home(request):
    return render(request, 'home.html')


def login1(request):
    return render(request, 'login1.html')


def register1(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confpassword = request.POST['confPassword']
        if password == confpassword:
            password = make_password(password)

        a = NewUser(name=name, username=username,
                    email=email, password=password)
        a.is_member = True
        a.save()
        messages.success(request, 'Account was created successfully')
        return redirect('home')

    return render(request, 'register1.html')
    # return render(request, 'register1.html')
